from django import forms
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline

from . import content_translations, languages
from .models import Differential, Doctor, Faq, Hospital, Page, Section, SiteSettings, Step, Testimonial

# Campos traduzidos aparecem em abas por idioma (Português, Español…). Campo
# vazio num idioma mostra o português no site — mas o idioma só fica público
# depois de marcado em Configurações do site → Idiomas publicados.

_BADGE = ('<span title="{title}" style="display:inline-block;margin:0 4px 2px 0;padding:1px 6px;'
          'border-radius:9px;font-size:11px;font-weight:600;white-space:nowrap;'
          'background:{bg};color:{fg}">{label}</span>')
_COLORS = {"done": ("#dcefdc", "#1e5e1e"), "partial": ("#fbecc8", "#7a5200"), "none": ("#ececec", "#666")}


def translation_badges(obj):
    """Uma etiqueta por idioma: ✓ completo, 3/5 parcial, – sem tradução."""
    parts = []
    for lang in languages.OPTIONAL:
        done, total = content_translations.status(obj, lang)
        short = languages.META[lang]["short"]
        if total and done == total:
            state, label, title = "done", f"{short} ✓", "traduzido"
        elif done:
            state, label, title = "partial", f"{short} {done}/{total}", f"{done} de {total} campos traduzidos"
        else:
            state, label, title = "none", f"{short} –", "sem tradução"
        bg, fg = _COLORS[state]
        parts.append(format_html(_BADGE, title=title, bg=bg, fg=fg, label=label))
    return format_html("".join(["{}"] * len(parts)), *parts)


class TranslationStatusMixin:
    """Acrescenta a coluna "Traduções" à lista do admin."""

    def get_list_display(self, request):
        return [*super().get_list_display(request), "translations"]

    @admin.display(description="Traduções")
    def translations(self, obj):
        return translation_badges(obj)


class SiteSettingsForm(forms.ModelForm):
    published = forms.MultipleChoiceField(
        label="Idiomas publicados",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[(code, name) for code, name in languages.settings.LANGUAGES
                 if code != languages.DEFAULT],
        help_text=SiteSettings._meta.get_field("published_languages").help_text,
    )

    class Meta:
        model = SiteSettings
        exclude = ["published_languages"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current = (self.instance.published_languages or "").split(",")
        self.fields["published"].initial = [c for c in current if c]

    def save(self, commit=True):
        self.instance.published_languages = ",".join(self.cleaned_data["published"])
        return super().save(commit)


@admin.register(SiteSettings)
class SiteSettingsAdmin(TabbedTranslationAdmin):
    form = SiteSettingsForm
    readonly_fields = ["translation_overview"]
    fieldsets = [
        ("Idiomas", {
            "fields": ["published", "translation_overview"],
            "description": "O português está sempre no ar. Para revisar um idioma antes "
            "de publicar, abra o site com o prefixo dele (/es/, /en/, /tr/) estando "
            "logado no admin.",
        }),
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

    @admin.display(description="Situação das traduções")
    def translation_overview(self, obj):
        rows = []
        for lang in languages.OPTIONAL:
            done, total = content_translations.overview(lang)
            pct = round(100 * done / total) if total else 0
            rows.append(format_html(
                "<li><strong>{}</strong>: {}% — {} de {} campos</li>",
                dict(settings.LANGUAGES)[lang], pct, done, total))
        return format_html(
            '<ul style="margin:0;padding-left:1.2em">{}</ul>'
            '<p class="help">Conta os textos do banco (páginas, seções, tratamentos, '
            "posts…). Campo sem tradução aparece em português. A coluna "
            "“Traduções” de cada lista mostra o que falta.</p>",
            format_html("".join(["{}"] * len(rows)), *rows))

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
SUFFIXES = [languages.field_suffix(code) for code in languages.ALL]


def _variants(name):
    """O campo e suas versões por idioma: title, title_pt_br, title_es…"""
    return [name] + [f"{name}_{sfx}" for sfx in SUFFIXES]


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
        for base in CONTENT_FIELDS:
            if base in used:
                continue
            for name in _variants(base):
                if name in self.fields:
                    # Para a imagem também funciona: sem arquivo enviado, o
                    # FileField mantém o valor atual.
                    self.fields[name].widget = forms.HiddenInput()


class SectionInline(TranslationStackedInline):
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
        for base in ("text", "body", "items"):
            for name in _variants(base):
                field = formset.form.base_fields.get(name)
                if field and not isinstance(field.widget, forms.HiddenInput):
                    field.widget.attrs.update(rows=4, cols=90)
        return formset


@admin.register(Page)
class PageAdmin(TranslationStatusMixin, TabbedTranslationAdmin):
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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("sections")

    @admin.display(description="No site")
    def view_link(self, obj):
        return format_html('<a href="{}" target="_blank">abrir ↗</a>', obj.get_absolute_url())

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderedAdmin(TranslationStatusMixin, TabbedTranslationAdmin):
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
