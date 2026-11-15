from modeltranslation.translator import TranslationOptions, register

from .models import Treatment


@register(Treatment)
class TreatmentTR(TranslationOptions):
    # O slug também é traduzido: /es/tratamientos/oncologia/ pode ter
    # endereço próprio em cada idioma.
    fields = ("slug", "title", "short", "intro", "procedures", "areas", "duration", "stay",
              "includes", "candidates", "seo_title")
    # Slug vazio vira NULL: o campo é único, e vários "" colidiriam.
    empty_values = {"slug": None}
