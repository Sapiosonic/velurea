from django.db import models
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext as _

from apps.core.models import OrderedModel


def _lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


class Treatment(OrderedModel):
    slug = models.SlugField(
        "endereço", max_length=80, unique=True,
        help_text="Parte final da URL: /tratamentos/<endereço>/. "
        "Mudar o endereço quebra links já compartilhados.",
    )
    title = models.CharField("nome", max_length=150)
    short = models.CharField(
        "resumo", max_length=250,
        help_text="Aparece no card da página inicial e como descrição no Google.",
    )
    intro = models.TextField("introdução")
    procedures = models.TextField("procedimentos disponíveis", help_text="Um por linha.")
    areas = models.TextField(
        "áreas atendidas", blank=True,
        help_text="Opcional. Um por linha (ex.: tipos de câncer em Oncologia).",
    )

    # ⚠️ Campos clínicos. Dependem de avaliação médica e variam caso a caso.
    # Deixe em branco até que a equipe médica confirme: num site de saúde,
    # inventar tempo de cirurgia ou critério de candidatura é afirmar algo
    # clinicamente falso. Em branco, a página simplesmente omite a seção.
    duration = models.CharField(
        "duração", max_length=100, blank=True,
        help_text="⚠️ Preencha somente com dado confirmado pela equipe médica.",
    )
    stay = models.CharField(
        "permanência estimada", max_length=100, blank=True,
        help_text="⚠️ Preencha somente com dado confirmado pela equipe médica.",
    )
    includes = models.TextField(
        "o que a coordenação inclui", blank=True,
        help_text="Opcional. Um por linha.",
    )
    candidates = models.TextField(
        "quem costuma ser candidato", blank=True,
        help_text="⚠️ Preencha somente com critério confirmado pela equipe médica.",
    )

    seo_title = models.CharField(
        "título na aba / Google", max_length=200, blank=True,
        help_text="Em branco: \"<nome> na Turquia — Velurea Clinic\".",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "tratamento"
        verbose_name_plural = "tratamentos"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("treatments:detail", args=[self.slug])

    @property
    def procedure_list(self):
        return _lines(self.procedures)

    @property
    def area_list(self):
        return _lines(self.areas)

    @property
    def include_list(self):
        return _lines(self.includes)

    @property
    def page_title(self):
        return self.seo_title or _("%(title)s na Turquia — Velurea Clinic") % {"title": self.title}

    @property
    def cta_title(self):
        # Minúsculas no meio da frase. Turco fica de fora: str.lower() erra
        # o İ/I turco, e a tradução pode reorganizar a frase de todo modo.
        title = self.title if get_language() == "tr" else self.title.lower()
        return _("Quer saber se %(title)s é indicado para você?") % {"title": title}

    @property
    def columns(self):
        """Listas da página de detalhe, na ordem do layout original."""
        cols = []
        if self.area_list:
            cols.append((_("Áreas atendidas"), self.area_list))
        cols.append((_("Procedimentos disponíveis"), self.procedure_list))
        if self.include_list:
            cols.append((_("O que a coordenação inclui"), self.include_list))
        return cols
