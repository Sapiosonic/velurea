from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post
from apps.treatments.models import Treatment


class StaticPagesSitemap(Sitemap):
    def items(self):
        return [
            "home", "sobre", "treatments:list", "medicos", "como_funciona",
            "depoimentos", "blog:list", "faq", "contato",
        ]

    def location(self, item):
        return reverse(item)


class TreatmentSitemap(Sitemap):
    def items(self):
        return Treatment.visible.all()


class PostSitemap(Sitemap):
    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {"pages": StaticPagesSitemap, "treatments": TreatmentSitemap, "blog": PostSitemap}
