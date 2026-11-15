"""Idiomas do site: quais existem, quais estão publicados e como se chamam.

`settings.LANGUAGES` diz quais idiomas o site *suporta*. Quais o público vê
é decisão do cliente, em Configurações do site → "Idiomas publicados".
"""

from django.conf import settings
from django.urls import translate_url
from django.utils import translation

DEFAULT = settings.LANGUAGE_CODE  # "pt-br"

# Sigla do seletor, atributo <html lang> / hreflang e og:locale.
META = {
    "pt-br": {"short": "PT", "html": "pt-BR", "hreflang": "pt-BR", "og": "pt_BR"},
    "es": {"short": "ES", "html": "es", "hreflang": "es", "og": "es_ES"},
    "en": {"short": "EN", "html": "en", "hreflang": "en", "og": "en_US"},
    "tr": {"short": "TR", "html": "tr", "hreflang": "tr", "og": "tr_TR"},
}

ALL = [code for code, _ in settings.LANGUAGES]
OPTIONAL = [code for code in ALL if code != DEFAULT]


def published(site=None):
    """Idiomas visíveis ao público, na ordem de settings.LANGUAGES."""
    if site is None:
        from .models import SiteSettings

        site = SiteSettings.load()
    chosen = {c for c in (site.published_languages or "").split(",") if c}
    return [code for code in ALL if code == DEFAULT or code in chosen]


def field_suffix(lang):
    """Sufixo das colunas do modeltranslation: 'pt-br' → 'pt_br'."""
    return lang.replace("-", "_")


def current():
    return translation.get_language() or DEFAULT


def find_by_slug(queryset, slug, field="slug"):
    """Busca pelo slug do idioma atual; se não achar, pelo slug em português.

    Devolve (objeto, redirecionar). `redirecionar` é True quando o objeto foi
    achado pelo slug em português mas tem slug próprio neste idioma — a view
    manda o visitante para o endereço traduzido (301).
    """
    lang_field = f"{field}_{field_suffix(current())}"
    obj = queryset.filter(**{lang_field: slug}).first()
    if obj is not None:
        return obj, False
    obj = queryset.filter(**{f"{field}_{field_suffix(DEFAULT)}": slug}).first()
    if obj is None:
        return None, False
    return obj, getattr(obj, field) != slug


def has_translation(obj, field, lang=None):
    """O campo tem texto próprio no idioma (sem contar o fallback)?"""
    return bool(getattr(obj, f"{field}_{field_suffix(lang or current())}", None))


def alternates_for_path(path, languages):
    """URL desta mesma página em cada idioma (resolve e reverte a rota)."""
    return {lang: translate_url(path, lang) for lang in languages}


def alternates_for_object(obj, languages):
    """URL de um objeto (tratamento, post) em cada idioma, com o slug traduzido."""
    urls = {}
    for lang in languages:
        with translation.override(lang):
            urls[lang] = obj.get_absolute_url()
    return urls


def prepopulated_slugs(slug, source):
    """prepopulated_fields do admin por idioma: slug_es nasce de title_es etc."""
    return {f"{slug}_{field_suffix(c)}": (f"{source}_{field_suffix(c)}",) for c in ALL}
