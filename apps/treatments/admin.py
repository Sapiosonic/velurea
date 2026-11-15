from django.contrib import admin

from .models import Treatment


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "order", "is_active"]
    list_editable = ["order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title", "procedures"]
    prepopulated_fields = {"slug": ["title"]}
    fieldsets = [
        (None, {"fields": ["title", "slug", "short", "intro", "is_active", "order"]}),
        ("Listas", {"fields": ["areas", "procedures", "includes"]}),
        ("Dados clínicos", {
            "fields": ["duration", "stay", "candidates"],
            "description": "⚠️ Preencha apenas com informação confirmada pela equipe "
            "médica. Campos em branco não aparecem no site.",
            "classes": ["collapse"],
        }),
        ("Google", {"fields": ["seo_title"], "classes": ["collapse"]}),
    ]
