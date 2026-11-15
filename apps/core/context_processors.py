from django.urls import reverse

from apps.treatments.models import Treatment

from .models import SiteSettings

NAV = [
    ("home", "Início"),
    ("sobre", "Sobre"),
    ("treatments:list", "Tratamentos"),
    ("medicos", "Médicos e Hospitais"),
    ("como_funciona", "Como Funciona"),
    ("depoimentos", "Depoimentos"),
    ("blog:list", "Blog"),
    ("faq", "FAQ"),
]


def site(request):
    """Dados usados pelo header e pelo rodapé de todas as páginas."""
    if request.path.startswith("/admin/"):
        return {}

    path = request.path
    nav = []
    for url_name, label in NAV:
        url = reverse(url_name)
        # Igual ao original: "Início" só fica ativo na própria home; os demais
        # também em subpáginas (/tratamentos/oncologia/ ativa "Tratamentos").
        active = path == url if url == "/" else path.startswith(url)
        nav.append({"url": url, "label": label, "active": active})

    return {
        "site": SiteSettings.load(),
        "nav": nav,
        "nav_treatments": Treatment.visible.only("slug", "title"),
    }
