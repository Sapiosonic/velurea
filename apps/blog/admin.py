from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin

from apps.core.admin import TranslationStatusMixin
from apps.core.languages import prepopulated_slugs

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(TranslationStatusMixin, TabbedTranslationAdmin):
    list_display = ["name", "slug", "post_count"]
    prepopulated_fields = prepopulated_slugs("slug", "name")

    @admin.display(description="posts")
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(TranslationStatusMixin, TabbedTranslationAdmin):
    list_display = ["title", "category", "status", "published_at", "view_link"]
    list_filter = ["status", "category"]
    search_fields = ["title", "excerpt", "body"]
    date_hierarchy = "published_at"
    prepopulated_fields = prepopulated_slugs("slug", "title")
    actions = ["publish", "unpublish"]
    fieldsets = [
        (None, {"fields": ["title", "slug", "category", "excerpt"]}),
        ("Artigo", {"fields": ["body"]}),
        ("Imagem de capa", {"fields": ["cover", "cover_alt"]}),
        ("Publicação", {"fields": ["status", "published_at", "reading_minutes"]}),
        ("Google", {"fields": ["seo_title"], "classes": ["collapse"]}),
    ]

    @admin.display(description="No site")
    def view_link(self, obj):
        label = "abrir ↗" if obj.is_live else "pré-visualizar ↗"
        return format_html('<a href="{}" target="_blank">{}</a>', obj.get_absolute_url(), label)

    @admin.action(description="Publicar selecionados")
    def publish(self, request, queryset):
        n = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f"{n} post(s) publicado(s).")

    @admin.action(description="Voltar para rascunho")
    def unpublish(self, request, queryset):
        n = queryset.update(status=Post.Status.DRAFT)
        self.message_user(request, f"{n} post(s) movido(s) para rascunho.")
