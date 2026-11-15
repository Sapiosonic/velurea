from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post
from apps.treatments.models import Treatment

from . import languages


class MultilingualSitemap(Sitemap):
    """Uma entrada por idioma publicado, com os links alternativos (hreflang)
    entre as versões — o formato que o Google recomenda para sites multilíngues."""

    i18n = True
    alternates = True
    x_default = True

    @property
    def languages(self):
        return languages.published()


class StaticPagesSitemap(MultilingualSitemap):
    def items(self):
        return [
            "home", "sobre", "treatments:list", "medicos", "como_funciona",
            "depoimentos", "blog:list", "faq", "contato",
        ]

    def location(self, item):
        return reverse(item)


class TreatmentSitemap(MultilingualSitemap):
    def items(self):
        return Treatment.visible.all()


class PostSitemap(MultilingualSitemap):
    def items(self):
        return Post.published.all()

    def get_languages_for_item(self, item):
        # Post só entra nos idiomas em que foi traduzido.
        return [code for code in self.languages if item.is_translated(code)]

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {"pages": StaticPagesSitemap, "treatments": TreatmentSitemap, "blog": PostSitemap}
