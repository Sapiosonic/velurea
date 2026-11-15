from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html

from .models import Differential, Doctor, Faq, Hospital, Page, Section, SiteSettings, Step, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Contato", {"fields": [
            "whatsapp_number", "whatsapp_display", "whatsapp_message",
            "email", "address", "hours", "languages_label",
        ]}),
        ("Rodapé", {"fields": ["footer_about", "footer_disclaimer"]}),
        ("Faixa de chamada (fim das páginas)", {
            "fields": ["cta_eyebrow", "cta_title", "cta_text"],
            "description": "Texto padrão. Cada página pode substituir título e texto.",
        }),
        ("Formulário e Google", {"fields": ["lead_notification_email", "noindex", "site_name"]}),
    ]

    # Registro único: a lista pula direto para a edição.
    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1, defaults=_settings_defaults())
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def _settings_defaults():
    from .seed import SETTINGS

    return SETTINGS


CONTENT_FIELDS = ["eyebrow", "title", "text", "body", "items", "note", "image", "image_alt"]


class SectionForm(forms.ModelForm):
    """Esconde os campos que o layout desta seção não exibe.

    Um campo escondido continua no formulário (com o valor atual), então
    salvar não apaga nada — só some da tela o que não teria efeito no site.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used = {f for f in (self.instance.used_fields or "").split(",") if f}
        if not used:
            return
        for name in CONTENT_FIELDS:
            if name not in used and name in self.fields:
                # Para a imagem também funciona: sem arquivo enviado, o
                # FileField mantém o valor atual.
                self.fields[name].widget = forms.HiddenInput()


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0
    can_delete = False
    fields = ["hint_display", "eyebrow", "title", "text", "body", "items", "note", "image", "image_alt"]
    readonly_fields = ["hint_display"]

    # Seções vêm do layout: editar sim, criar não.
    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description="Campos usados")
    def hint_display(self, obj):
        return obj.hint or "—"

    def get_formset(self, request, obj=None, **kwargs):
        kwargs["form"] = SectionForm
        formset = super().get_formset(request, obj, **kwargs)
        for name in ("text", "body", "items"):
            if name in formset.form.base_fields:
                formset.form.base_fields[name].widget.attrs.update(rows=4, cols=90)
        return formset


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["name", "seo_title", "view_link"]
    inlines = [SectionInline]
    fieldsets = [
        ("Google e compartilhamento", {
            "fields": ["seo_title", "seo_description", "og_title", "og_description"],
            "classes": ["collapse"],
        }),
        ("Faixa de chamada no fim da página", {
            "fields": ["cta_title", "cta_text"],
            "classes": ["collapse"],
        }),
    ]

    @admin.display(description="No site")
    def view_link(self, obj):
        return format_html('<a href="{}" target="_blank">abrir ↗</a>', obj.get_absolute_url())

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ["order", "is_active"]
    list_filter = ["is_active"]


@admin.register(Step)
class StepAdmin(OrderedAdmin):
    list_display = ["title", "number", "order", "is_active"]

    @admin.display(description="nº no site")
    def number(self, obj):
        visible = list(Step.visible.values_list("pk", flat=True))
        return f"{visible.index(obj.pk) + 1:02d}" if obj.pk in visible else "—"


@admin.register(Differential)
class DifferentialAdmin(OrderedAdmin):
    list_display = ["title", "order", "is_active"]


@admin.register(Testimonial)
class TestimonialAdmin(OrderedAdmin):
    list_display = ["name", "origin", "treatment", "on_home", "order", "is_active"]
    list_editable = ["on_home", "order", "is_active"]


@admin.register(Faq)
class FaqAdmin(OrderedAdmin):
    list_display = ["question", "order", "is_active"]


@admin.register(Doctor)
class DoctorAdmin(OrderedAdmin):
    list_display = ["name", "role", "order", "is_active"]


@admin.register(Hospital)
class HospitalAdmin(OrderedAdmin):
    list_display = ["name", "order", "is_active"]
