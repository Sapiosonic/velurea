"""Carrega o conteúdo inicial do site (o mesmo da versão estática).

Seguro de rodar mais de uma vez: só cria o que ainda não existe e nunca
sobrescreve um texto já editado no admin. Para recomeçar do zero, use
`--reset`, que apaga o conteúdo (não apaga contatos recebidos nem usuários).
"""

import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone, translation
from django.utils.text import slugify

from apps.blog.models import Category, Post
from apps.blog.seed_posts import BODIES
from apps.core import seed
from apps.core.admin import CONTENT_FIELDS
from apps.core.models import (
    Differential, Doctor, Faq, Hospital, Page, Section, SiteSettings, Step, Testimonial,
)
from apps.treatments.models import Treatment

PAGE_FIELDS = ["name", "url_name", "seo_title", "seo_description", "og_title",
               "og_description", "cta_title", "cta_text"]


class Command(BaseCommand):
    help = "Carrega o conteúdo inicial do site Velurea."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Apaga o conteúdo existente antes de carregar.")

    def handle(self, *args, reset=False, **opts):
        # O conteúdo inicial é português. Com o modeltranslation, `title=...`
        # grava na coluna do idioma ativo — então o idioma é fixado aqui, em
        # vez de depender de quem chamou o comando.
        with translation.override(settings.LANGUAGE_CODE):
            self._load(reset)

    @transaction.atomic
    def _load(self, reset):
        if reset:
            for model in (Section, Page, Treatment, Step, Differential, Testimonial,
                          Faq, Doctor, Hospital, Post, Category, SiteSettings):
                model.objects.all().delete()

        SiteSettings.objects.get_or_create(pk=1, defaults=seed.SETTINGS)

        for order, data in enumerate(seed.PAGES):
            data = dict(data)
            sections = data.pop("sections")
            key = data.pop("key")
            page, _ = Page.objects.get_or_create(
                key=key,
                defaults={"order": order, **{f: data.get(f, "") for f in PAGE_FIELDS}},
            )
            for s_order, sec in enumerate(sections):
                sec = dict(sec)
                section, _ = Section.objects.get_or_create(
                    page=page, key=sec.pop("key"), defaults={"order": s_order, **sec}
                )
                # Metadados de layout (não são conteúdo): sempre atualizados,
                # para acompanhar mudanças nos templates.
                used = [f for f in CONTENT_FIELDS if sec.get(f)]
                if "image_alt" in used:
                    used.append("image")
                section.label = sec["label"]
                section.hint = sec.get("hint", "")
                section.used_fields = ",".join(used)
                section.save(update_fields=["label", "hint", "used_fields"])

        if not Treatment.objects.exists():
            for order, t in enumerate(seed.TREATMENTS):
                Treatment.objects.create(
                    order=order, slug=t["slug"], title=t["title"], short=t["short"],
                    intro=t["intro"], procedures="\n".join(t["procedures"]),
                    areas="\n".join(t.get("areas", [])),
                )

        self._simple(Step, seed.STEPS, ["title", "text"])
        self._simple(Differential, seed.DIFFERENTIALS, ["title", "text"])
        self._simple(Testimonial, seed.TESTIMONIALS, ["name", "origin", "treatment", "quote", "on_home"])
        self._simple(Faq, seed.FAQS, ["question", "answer"])
        self._simple(Doctor, seed.DOCTORS, ["name", "role", "detail"])
        self._simple(Hospital, seed.HOSPITALS, ["name", "detail"])

        if not Post.objects.exists():
            tz = timezone.get_current_timezone()
            for slug, title, excerpt, cat_name, date, minutes in seed.POSTS:
                category, _ = Category.objects.get_or_create(
                    name=cat_name, defaults={"slug": slugify(cat_name)}
                )
                Post.objects.create(
                    slug=slug, title=title, excerpt=excerpt, category=category,
                    status=Post.Status.PUBLISHED, body=BODIES.get(slug, ""),
                    published_at=datetime.datetime.fromisoformat(date).replace(hour=9, tzinfo=tz),
                )

        # Bancos criados antes de os artigos terem texto: preenche só o que
        # ainda está vazio, sem tocar em texto escrito no admin.
        for post in Post.objects.filter(slug__in=BODIES, body=""):
            post.body = BODIES[post.slug]
            post.reading_minutes = None
            post.save()

        self.stdout.write(self.style.SUCCESS("Conteúdo inicial carregado."))

    def _simple(self, model, rows, fields):
        if model.objects.exists():
            return
        for order, row in enumerate(rows):
            model.objects.create(order=order, **dict(zip(fields, row)))

