from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
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
        path("categoria/<slug:category_slug>/", blog_views.post_list, name="category"),
        path("<slug:slug>/", blog_views.post_detail, name="detail"),
    ],
    "blog",
)

urlpatterns = [
    path("", core.home, name="home"),
    path("sobre/", core.sobre, name="sobre"),
    path("tratamentos/", include(treatment_urls)),
    path("como-funciona/", core.como_funciona, name="como_funciona"),
    path("depoimentos/", core.depoimentos, name="depoimentos"),
    path("medicos-e-hospitais/", core.medicos, name="medicos"),
    path("blog/", include(blog_urls)),
    path("perguntas-frequentes/", core.faq, name="faq"),
    path("contato/", contact_views.contato, name="contato"),
    path("obrigado/", core.obrigado, name="obrigado"),
    path("robots.txt", core.robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico", permanent=True)),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.core.views.page_not_found"
