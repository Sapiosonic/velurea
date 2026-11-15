from django.conf import settings
from django.test import TestCase as DjangoTestCase
from django.utils import translation


class TestCase(DjangoTestCase):
    """Cada teste começa (e termina) em português.

    O LocaleMiddleware ativa o idioma da requisição e não o desfaz ao final;
    num servidor, a próxima requisição ativa o dela. Nos testes, porém, o
    código do próprio teste roda na mesma thread — e o modeltranslation
    traduz `filter(slug=...)` para a coluna do idioma ativo. Sem este reset,
    uma requisição em /es/ mudaria o resultado das consultas seguintes.
    """

    @classmethod
    def setUpClass(cls):
        translation.activate(settings.LANGUAGE_CODE)
        super().setUpClass()

    def setUp(self):
        super().setUp()
        translation.activate(settings.LANGUAGE_CODE)
        self.addCleanup(translation.activate, settings.LANGUAGE_CODE)
