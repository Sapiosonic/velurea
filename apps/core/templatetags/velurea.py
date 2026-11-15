"""Filtros e tags dos templates do site (carregados em todo template)."""

import re

from django import template
from django.templatetags.static import static
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()

# Ícones Lucide, idênticos aos do site original (mesmo desenho, mesma classe
# `lucide lucide-<nome>`), para que o CSS compilado continue valendo.
ICONS = {
    "message-circle": '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"></path>',
    "menu": '<path d="M4 5h16"></path><path d="M4 12h16"></path><path d="M4 19h16"></path>',
    "mail": '<path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"></path><rect x="2" y="4" width="20" height="16" rx="2"></rect>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle>',
    "clock": '<circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path>',
    "arrow-right": '<path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>',
    "arrow-left": '<path d="m12 19-7-7 7-7"></path><path d="M19 12H5"></path>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path><path d="m9 12 2 2 4-4"></path>',
    "languages": '<path d="m5 8 6 6"></path><path d="m4 14 6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="m22 22-5-10-5 10"></path><path d="M14 18h6"></path>',
    "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path>',
    "heart-pulse": '<path d="M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5"></path><path d="M3.22 13H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"></path>',
    "circle-check": '<circle cx="12" cy="12" r="10"></circle><path d="m9 12 2 2 4-4"></path>',
    "chevron-down": '<path d="m6 9 6 6 6-6"></path>',
    "check": '<path d="M20 6 9 17l-5-5"></path>',
}


@register.simple_tag
def icon(name, css="", stroke="2"):
    return format_html(
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="{}" stroke-linecap="round" '
        'stroke-linejoin="round" class="lucide lucide-{} {}" aria-hidden="true">{}</svg>',
        stroke, name, css, mark_safe(ICONS[name]),
    )


_BOLD = re.compile(r"\*\*(.+?)\*\*")


@register.filter
def rich(value, strong_class="text-foreground"):
    """Escapa o texto e transforma **trecho** em <strong>.

    É a única marcação aceita nos campos de texto das seções: o cliente
    consegue destacar uma expressão sem poder injetar HTML.
    """
    escaped = str(conditional_escape(value or ""))
    cls = conditional_escape(strong_class)
    return mark_safe(_BOLD.sub(rf'<strong class="{cls}">\1</strong>', escaped))


@register.filter
def paragraphs(value):
    """Divide um texto em parágrafos separados por linha em branco."""
    return [p.strip() for p in re.split(r"\n\s*\n", value or "") if p.strip()]


@register.simple_tag
def image_url(section, default_static):
    """URL da imagem enviada no admin, ou da imagem original do site."""
    if section is not None and getattr(section, "image", None):
        return section.image.url
    return static(default_static)


# ------------------------------------------------------------- idiomas ---

# Data longa por idioma. Português e espanhol escrevem o mês em minúsculas
# ("12 de março de 2026"); inglês e turco, com inicial maiúscula.
LONG_DATE = {
    "pt-br": ("j \d\e F \d\e Y", True),
    "es": ("j \d\e F \d\e Y", True),
    "en": ("F j, Y", False),
    "tr": ("j F Y", False),
}


@register.filter
def long_date(value):
    from django.utils import dateformat, timezone

    from apps.core import languages

    if not value:
        return ""
    fmt, lower = LONG_DATE.get(languages.current(), LONG_DATE[languages.DEFAULT])
    text = dateformat.format(timezone.localtime(value), fmt)
    return text.lower() if lower else text


@register.simple_tag(takes_context=True)
def language_versions(context):
    """Versões desta página em cada idioma, para o seletor e o hreflang.

    A view pode informar `alternates` (tratamentos e posts, cujo slug muda por
    idioma); senão, a URL é traduzida a partir da rota atual.
    """
    from apps.core import languages

    request = context["request"]
    published = getattr(request, "published_languages", [languages.DEFAULT])
    is_staff = request.user.is_authenticated and request.user.is_staff
    # Quem está no admin navega também pelos idiomas ainda não publicados.
    visible = languages.ALL if is_staff else published

    alternates = context.get("alternates")
    if alternates is None:
        alternates = languages.alternates_for_path(request.path, visible)
    current = languages.current()

    versions = []
    for code in languages.ALL:
        if code not in alternates or code not in visible:
            continue
        meta = languages.META[code]
        versions.append({
            "code": code,
            "short": meta["short"],
            "hreflang": meta["hreflang"],
            "og": meta["og"],
            "url": alternates[code],
            "absolute_url": request.build_absolute_uri(alternates[code]),
            "current": code == current,
            "published": code in published,
        })
    return versions
