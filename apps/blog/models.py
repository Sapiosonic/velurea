import math

import nh3
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from tinymce.models import HTMLField

# O corpo do post vem de um editor visual e é exibido como HTML. Mesmo vindo do
# admin, passa por uma lista de tags permitidas: um <script> colado por engano
# (de um embed, de outro site) não chega à página pública.
ALLOWED_TAGS = {
    "p", "br", "h2", "h3", "h4", "strong", "b", "em", "i", "u", "s",
    "ul", "ol", "li", "blockquote", "a", "img", "figure", "figcaption",
    "hr", "table", "thead", "tbody", "tr", "th", "td",
}
ALLOWED_ATTRIBUTES = {
    "a": {"href", "title", "target"},
    "img": {"src", "alt", "title", "width", "height"},
    "th": {"colspan", "rowspan"},
    "td": {"colspan", "rowspan"},
}


def clean_html(value: str) -> str:
    return nh3.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        link_rel="noopener noreferrer",
    )


class Category(models.Model):
    name = models.CharField("nome", max_length=80)
    slug = models.SlugField("endereço", max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())
            .select_related("category")
        )

    def for_language(self, lang):
        """Publicados que têm tradução no idioma. Português: todos."""
        qs = self.get_queryset()
        if lang == settings.LANGUAGE_CODE:
            return qs
        title = f"title_{lang.replace('-', '_')}"
        return qs.exclude(**{f"{title}__isnull": True}).exclude(**{title: ""})


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        PUBLISHED = "published", "Publicado"

    title = models.CharField("título", max_length=200)
    slug = models.SlugField(
        "endereço", max_length=200, unique=True,
        help_text="Parte final da URL: /blog/<endereço>/. Gerado a partir do título.",
    )
    category = models.ForeignKey(
        Category, verbose_name="categoria", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="posts",
    )
    excerpt = models.TextField(
        "resumo", max_length=400,
        help_text="Aparece na lista do blog e como descrição no Google.",
    )
    cover = models.ImageField("imagem de capa", upload_to="blog/", blank=True)
    cover_alt = models.CharField("descrição da imagem de capa", max_length=200, blank=True)
    body = HTMLField("texto do artigo", blank=True)

    status = models.CharField(
        "situação", max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    published_at = models.DateTimeField(
        "data de publicação", default=timezone.now,
        help_text="Uma data futura agenda a publicação.",
    )
    reading_minutes = models.PositiveSmallIntegerField(
        "tempo de leitura (min)", null=True, blank=True,
        help_text="Em branco, é calculado pelo tamanho do texto.",
    )

    seo_title = models.CharField(
        "título na aba / Google", max_length=200, blank=True,
        help_text="Em branco, usa o título do post.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Higieniza o corpo em todos os idiomas (body_pt_br, body_es…).
        for code, _ in settings.LANGUAGES:
            field = f"body_{code.replace('-', '_')}"
            value = getattr(self, field, None)
            if value:
                setattr(self, field, clean_html(value))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.slug])

    @property
    def is_live(self):
        return self.status == self.Status.PUBLISHED and self.published_at <= timezone.now()

    def is_translated(self, lang):
        if lang == settings.LANGUAGE_CODE:
            return True
        return bool(getattr(self, f"title_{lang.replace('-', '_')}", None))

    @property
    def reading_time(self):
        if self.reading_minutes:
            return self.reading_minutes
        words = len(strip_tags(self.body or self.excerpt).split())
        return max(1, math.ceil(words / 200))

    @property
    def page_title(self):
        return self.seo_title or f"{self.title} | Velurea Clinic"
