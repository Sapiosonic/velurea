"""Painel inicial do admin: números do dia a dia e atalhos.

Cada cartão só aparece para quem tem permissão de ver aquele conteúdo.
"""

from django import template
from django.conf import settings
from django.urls import reverse

from apps.core import content_translations, languages

register = template.Library()


@register.inclusion_tag("admin/velurea_dashboard.html", takes_context=True)
def velurea_dashboard(context):
    from apps.blog.models import Post
    from apps.contact.models import Lead
    from apps.core.models import SiteSettings

    user = context["request"].user
    site = SiteSettings.load()
    stats, actions = [], []

    if user.has_perm("contact.view_lead"):
        new = Lead.objects.filter(status=Lead.Status.NEW).count()
        stats.append({
            "label": "Contatos novos",
            "value": new,
            "hint": "aguardando atendimento" if new else "nenhum pendente",
            "url": reverse("admin:contact_lead_changelist") + "?status__exact=new",
            "highlight": bool(new),
        })

    if user.has_perm("blog.view_post"):
        published = Post.objects.filter(status=Post.Status.PUBLISHED).count()
        drafts = Post.objects.filter(status=Post.Status.DRAFT).count()
        stats.append({
            "label": "Posts publicados",
            "value": published,
            "hint": f"{drafts} rascunho{'s' if drafts != 1 else ''}",
            "url": reverse("admin:blog_post_changelist"),
        })
        if user.has_perm("blog.add_post"):
            actions.append({"label": "Novo post", "url": reverse("admin:blog_post_add"), "primary": True})

    if user.has_perm("core.view_sitesettings"):
        names = dict(settings.LANGUAGES)
        langs = []
        for code in languages.OPTIONAL:
            done, total = content_translations.overview(code)
            langs.append({
                "short": languages.META[code]["short"],
                "name": names[code],
                "pct": round(100 * done / total) if total else 0,
                "published": code in languages.published(site),
            })
        stats.append({
            "label": "Idiomas no ar",
            "value": len(languages.published(site)),
            "hint": "de 4 disponíveis",
            "url": reverse("admin:core_sitesettings_changelist"),
            "languages": langs,
        })

    if user.has_perm("core.change_page"):
        actions.append({"label": "Editar páginas", "url": reverse("admin:core_page_changelist")})
    if user.has_perm("core.change_sitesettings"):
        actions.append({"label": "Configurações do site", "url": reverse("admin:core_sitesettings_changelist")})

    return {
        "user": user,
        "stats": stats,
        "actions": actions,
        "site_url": context.get("site_url") or "/",
        "noindex": site.noindex and user.has_perm("core.view_sitesettings"),
        "settings_url": reverse("admin:core_sitesettings_changelist"),
    }
