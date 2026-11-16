"""Traduções do conteúdo do banco em arquivo (locale/content/<idioma>.json).

O conteúdo editável mora no banco, e o banco não vai para o repositório.
Para que uma tradução feita fora do admin (por um tradutor com planilha, ou
um rascunho gerado por IA) chegue a qualquer instalação, ela fica num JSON
versionado e é carregada por `seed_site` ou `import_content`.

Formato: {modelo: {chave: {campo: texto}}}. A chave identifica o registro
pelo seu texto/endereço em português (não pelo id, que muda de banco para
banco). Se o cliente reescrever o original em português, a chave deixa de
bater e a tradução antiga simplesmente não é aplicada — melhor do que
aplicar a tradução de um texto que já não existe.

A importação só preenche campos vazios, a menos que se peça `overwrite`:
o que foi escrito no admin nunca é sobrescrito sem querer.
"""

import json
from pathlib import Path

from django.conf import settings
from django.db import transaction

from apps.blog.models import Category, Post
from apps.treatments.models import Treatment

from . import languages
from .models import Differential, Doctor, Faq, Hospital, Page, Section, SiteSettings, Step, Testimonial

CONTENT_DIR = Path(settings.BASE_DIR) / "locale" / "content"

PT = languages.field_suffix(languages.DEFAULT)

# modelo → (nome no arquivo, função que dá a chave, campos traduzíveis)
REGISTRY = [
    (SiteSettings, "site", lambda o: "site",
     ["whatsapp_message", "address", "hours", "footer_about", "footer_disclaimer",
      "cta_eyebrow", "cta_title", "cta_text"]),
    (Page, "page", lambda o: o.key,
     ["seo_title", "seo_description", "og_title", "og_description", "cta_title", "cta_text"]),
    (Section, "section", lambda o: f"{o.page.key}/{o.key}",
     ["eyebrow", "title", "text", "body", "items", "note", "image_alt"]),
    (Treatment, "treatment", lambda o: getattr(o, f"slug_{PT}"),
     ["slug", "title", "short", "intro", "procedures", "areas", "duration", "stay",
      "includes", "candidates", "seo_title"]),
    (Step, "step", lambda o: getattr(o, f"title_{PT}"), ["title", "text"]),
    (Differential, "differential", lambda o: getattr(o, f"title_{PT}"), ["title", "text"]),
    (Testimonial, "testimonial", lambda o: o.name, ["treatment"]),
    (Faq, "faq", lambda o: getattr(o, f"question_{PT}"), ["question", "answer"]),
    (Doctor, "doctor", lambda o: o.name, ["role", "detail"]),
    (Hospital, "hospital", lambda o: getattr(o, f"name_{PT}"), ["name", "detail"]),
    (Category, "category", lambda o: getattr(o, f"slug_{PT}"), ["name", "slug"]),
    (Post, "post", lambda o: getattr(o, f"slug_{PT}"),
     ["title", "slug", "excerpt", "body", "cover_alt", "seo_title"]),
]


def is_translated(obj, field, lang):
    """O campo tem texto próprio em `lang`?

    Texto igual ao português conta como "não traduzido": campos com valor
    padrão no model (Configurações do site) nascem com o padrão em português
    copiado para todas as colunas de idioma.
    """
    value = getattr(obj, f"{field}_{languages.field_suffix(lang)}")
    if not value:
        return False
    # Só para campos com padrão: "Blog", "FAQ" ou "Abdominoplastia" são
    # legitimamente iguais em português e espanhol.
    if obj._meta.get_field(field).has_default():
        return value != getattr(obj, f"{field}_{PT}")
    return True


def _queryset(model):
    qs = model.objects.all()
    if model is Section:
        qs = qs.select_related("page")
    return qs


def export(lang, source=languages.DEFAULT):
    """Textos em `source` (português) de tudo o que é traduzível, sem vazios."""
    src = languages.field_suffix(source)
    data = {}
    for model, name, key, fields in REGISTRY:
        rows = {}
        for obj in _queryset(model):
            values = {f: getattr(obj, f"{f}_{src}") for f in fields}
            values = {f: v for f, v in values.items() if v}
            if values:
                rows[key(obj)] = values
        if rows:
            data[name] = rows
    return data


@transaction.atomic
def apply(lang, data, overwrite=False):
    """Grava as traduções de `data` nas colunas de `lang`. Devolve contagens."""
    suffix = languages.field_suffix(lang)
    filled = skipped = missing = 0
    for model, name, key, fields in REGISTRY:
        rows = data.get(name) or {}
        if not rows:
            continue
        for obj in _queryset(model):
            values = rows.get(key(obj))
            if not values:
                continue
            changed = []
            for field, text in values.items():
                if field not in fields or not text:
                    continue
                column = f"{field}_{suffix}"
                if is_translated(obj, field, lang) and not overwrite:
                    skipped += 1
                    continue
                setattr(obj, column, text)
                changed.append(column)
            if changed:
                obj.save()
                filled += len(changed)
        known = {key(o) for o in _queryset(model)}
        missing += sum(1 for k in rows if k not in known)
    return {"filled": filled, "skipped": skipped, "missing": missing}


def available():
    """Idiomas com arquivo de tradução de conteúdo."""
    return [code for code in languages.OPTIONAL if (CONTENT_DIR / f"{code}.json").exists()]


def load_file(lang):
    with open(CONTENT_DIR / f"{lang}.json", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- situação

_BY_MODEL = {model: fields for model, _name, _key, fields in REGISTRY}


def _counted_fields(model):
    # O endereço (slug) não conta: em branco, o site usa o endereço em
    # português, e muitas vezes ele é igual nos dois idiomas.
    return [f for f in _BY_MODEL.get(model, []) if f != "slug"]


def status(obj, lang):
    """(traduzidos, total) dos campos com texto em português deste registro.

    Uma página inclui as suas seções.
    """
    objs = [obj]
    if isinstance(obj, Page):
        objs += list(obj.sections.all())
    done = total = 0
    for item in objs:
        for field in _counted_fields(type(item)):
            if not getattr(item, f"{field}_{PT}"):
                continue
            total += 1
            done += is_translated(item, field, lang)
    return done, total


def overview(lang):
    """(traduzidos, total) somando todo o conteúdo do site."""
    done = total = 0
    for model, *_ in REGISTRY:
        if model is Section:  # contadas junto com a página
            continue
        for obj in _queryset(model):
            d, t = status(obj, lang)
            done += d
            total += t
    return done, total
