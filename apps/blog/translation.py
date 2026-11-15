from modeltranslation.translator import TranslationOptions, register

from .models import Category, Post


@register(Category)
class CategoryTR(TranslationOptions):
    fields = ("name", "slug")
    empty_values = {"slug": None}


@register(Post)
class PostTR(TranslationOptions):
    # Um post só aparece num idioma quando tem título naquele idioma — veja
    # Post.published.for_language(). Não há "post em português dentro do blog
    # em espanhol".
    fields = ("title", "slug", "excerpt", "body", "cover_alt", "seo_title")
    empty_values = {"slug": None}
