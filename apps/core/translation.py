"""Campos do app core traduzidos pelo admin (django-modeltranslation).

Cada campo listado ganha uma coluna por idioma (title_pt_br, title_es…) e
abas no admin. Ficam de fora, de propósito:
* nomes próprios (pacientes, médicos) e o texto dos depoimentos, que é
  publicado no idioma em que o paciente escreveu;
* dados de contato que não mudam com o idioma (número, e-mail).
"""

from modeltranslation.translator import TranslationOptions, register

from .models import Differential, Doctor, Faq, Hospital, Page, Section, SiteSettings, Step, Testimonial


@register(SiteSettings)
class SiteSettingsTR(TranslationOptions):
    fields = ("whatsapp_message", "address", "hours", "footer_about", "footer_disclaimer",
              "cta_eyebrow", "cta_title", "cta_text")


@register(Page)
class PageTR(TranslationOptions):
    fields = ("seo_title", "seo_description", "og_title", "og_description", "cta_title", "cta_text")


@register(Section)
class SectionTR(TranslationOptions):
    fields = ("eyebrow", "title", "text", "body", "items", "note", "image_alt")


@register(Step)
class StepTR(TranslationOptions):
    fields = ("title", "text")


@register(Differential)
class DifferentialTR(TranslationOptions):
    fields = ("title", "text")


@register(Testimonial)
class TestimonialTR(TranslationOptions):
    fields = ("treatment",)


@register(Faq)
class FaqTR(TranslationOptions):
    fields = ("question", "answer")


@register(Doctor)
class DoctorTR(TranslationOptions):
    fields = ("role", "detail")


@register(Hospital)
class HospitalTR(TranslationOptions):
    fields = ("name", "detail")
