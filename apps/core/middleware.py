from django.conf import settings
from django.http import Http404
from django.utils import translation

from . import languages
from .models import SiteSettings

# Áreas fora das rotas por idioma. O admin fica sempre em português (os
# rótulos dos campos são escritos em português), independente do navegador.
UNTRANSLATED_PREFIXES = ("/admin/", "/tinymce/")


class LanguageGateMiddleware:
    """Esconde do público os idiomas ainda não publicados.

    Quem está logado no admin vê qualquer idioma — é a pré-visualização da
    tradução antes de publicar.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(UNTRANSLATED_PREFIXES):
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
            return self.get_response(request)

        site = SiteSettings.load()
        request.site_settings = site
        request.published_languages = languages.published(site)

        lang = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
        is_staff = request.user.is_authenticated and request.user.is_staff
        request.language_preview = lang not in request.published_languages
        if request.language_preview and not is_staff:
            raise Http404
        return self.get_response(request)
