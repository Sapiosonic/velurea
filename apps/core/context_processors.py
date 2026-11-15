from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.treatments.models import Treatment

from . import languages
from .models import SiteSettings

NAV = [
    ("home", _("Início")),
    ("sobre", _("Sobre")),
    ("treatments:list", _("Tratamentos")),
    ("medicos", _("Médicos e Hospitais")),
    ("como_funciona", _("Como Funciona")),
    ("depoimentos", _("Depoimentos")),
    ("blog:list", _("Blog")),
    ("faq", _("FAQ")),
]


def site(request):
    """Dados usados pelo header e pelo rodapé de todas as páginas."""
    if request.path.startswith("/admin/"):
        return {}

    path = request.path
    home = reverse("home")
    nav = []
    for url_name, label in NAV:
        url = reverse(url_name)
        # Igual ao original: "Início" só fica ativo na própria home; os demais
        # também em subpáginas (/tratamentos/oncologia/ ativa "Tratamentos").
        active = path == url if url == home else path.startswith(url)
        nav.append({"url": url, "label": label, "active": active})

    lang = languages.current()
    return {
        "site": getattr(request, "site_settings", None) or SiteSettings.load(),
        "nav": nav,
        "nav_treatments": Treatment.visible.all(),
        "lang": languages.META.get(lang, languages.META[languages.DEFAULT]),
        "language_preview": getattr(request, "language_preview", False),
    }
