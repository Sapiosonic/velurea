"""Exporta o conteúdo em português para tradução fora do admin.

    python manage.py export_content -o para-traduzir.json

Traduza os valores (mantendo chaves, nomes de campo, `**negrito**`, `|` e
quebras de linha) e salve como locale/content/<idioma>.json.
"""

import json

from django.core.management.base import BaseCommand
from django.utils import translation

from apps.core import content_translations, languages


class Command(BaseCommand):
    help = "Exporta, em JSON, o texto em português de todo o conteúdo traduzível."

    def add_arguments(self, parser):
        parser.add_argument("-o", "--output", required=True, help="Arquivo JSON de saída.")

    def handle(self, *args, output, **opts):
        with translation.override(languages.DEFAULT):
            data = content_translations.export(languages.DEFAULT)
        # Arquivo em UTF-8: o console do Windows não imprime "ş", "ğ"…
        with open(output, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        self.stdout.write(f"Exportado para {output}.")
