"""Carrega traduções de conteúdo de locale/content/<idioma>.json.

    python manage.py import_content es          # só preenche campos vazios
    python manage.py import_content es --overwrite

Sem idioma, carrega todos os arquivos existentes.
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import translation

from apps.core import content_translations, languages


class Command(BaseCommand):
    help = "Importa traduções de conteúdo (locale/content/<idioma>.json) para o banco."

    def add_arguments(self, parser):
        parser.add_argument("langs", nargs="*", help="Idiomas (padrão: todos com arquivo).")
        parser.add_argument("--overwrite", action="store_true",
                            help="Substitui também campos já traduzidos no admin.")

    def handle(self, *args, langs=None, overwrite=False, **opts):
        langs = langs or content_translations.available()
        for lang in langs:
            if lang not in languages.OPTIONAL:
                raise CommandError(f"Idioma desconhecido: {lang}")
            with translation.override(languages.DEFAULT):
                result = content_translations.apply(
                    lang, content_translations.load_file(lang), overwrite=overwrite)
            self.stdout.write(
                f"{lang}: {result['filled']} campos preenchidos, "
                f"{result['skipped']} já traduzidos (mantidos), "
                f"{result['missing']} registros não encontrados."
            )
