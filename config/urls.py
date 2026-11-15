from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.text import format_lazy
from django.utils.translation import pgettext_lazy
from django.views.generic import RedirectView

from apps.blog import views as blog_views
from apps.contact import views as contact_views
from apps.core import views as core
from apps.core.sitemaps import sitemaps
from apps.treatments import views as treatment_views

admin.site.site_header = "Velurea Clinic — Administração do site"
admin.site.site_title = "Velurea Admin"
admin.site.index_title = "Conteúdo do site"
admin.site.site_url = "/"


# Trechos de URL traduzíveis: pgettext_lazy("url", "sobre/"). O texto em
# português é a URL do idioma padrão e a chave da tradução; o contexto "url"
# separa estes textos dos textos de tela nos arquivos .po
# (locale/<idioma>/LC_MESSAGES/django.po). A chamada precisa ser escrita por
# extenso, com texto literal, para o makemessages encontrar.


treatment_urls = (
    [
        path("", treatment_views.treatment_list, name="list"),
        path("<slug:slug>/", treatment_views.treatment_detail, name="detail"),
    ],
    "treatments",
)

blog_urls = (
    [
        path("", blog_views.post_list, name="list"),
        path(format_lazy("{}<slug:category_slug>/", pgettext_lazy("url", "categoria/")), blog_views.post_list, name="category"),
        path("<slug:slug>/", blog_views.post_detail, name="detail"),
    ],
    "blog",
)

# Fora do prefixo de idioma: arquivos técnicos e o admin.
urlpatterns = [
    path("robots.txt", core.robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico", permanent=True)),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
]

# Páginas do site. Português sem prefixo (/contato/, como sempre foi); os
# demais idiomas com prefixo e caminho traduzido (/es/contacto/).
urlpatterns += i18n_patterns(
    path("", core.home, name="home"),
    path(pgettext_lazy("url", "sobre/"), core.sobre, name="sobre"),
    path(pgettext_lazy("url", "tratamentos/"), include(treatment_urls)),
    path(pgettext_lazy("url", "como-funciona/"), core.como_funciona, name="como_funciona"),
    path(pgettext_lazy("url", "depoimentos/"), core.depoimentos, name="depoimentos"),
    path(pgettext_lazy("url", "medicos-e-hospitais/"), core.medicos, name="medicos"),
    path(pgettext_lazy("url", "blog/"), include(blog_urls)),
    path(pgettext_lazy("url", "perguntas-frequentes/"), core.faq, name="faq"),
    path(pgettext_lazy("url", "contato/"), contact_views.contato, name="contato"),
    path(pgettext_lazy("url", "obrigado/"), core.obrigado, name="obrigado"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.page_not_found"
