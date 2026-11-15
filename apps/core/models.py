"""Conteúdo institucional editável pelo admin.

Três tipos de conteúdo:

* `SiteSettings` — dados que aparecem em todas as páginas (contato, rodapé).
  Existe um registro só.
* `Page` + `Section` — o texto fixo de cada página. O conjunto de páginas e de
  seções é definido pelo layout, então o admin permite *editar* mas não criar
  nem apagar: uma seção apagada deixaria um buraco no layout.
* Coleções (`Step`, `Differential`, `Testimonial`, `Faq`, `Doctor`,
  `Hospital`) — listas que o cliente pode aumentar, reordenar e ocultar.
"""

import urllib.parse

from django.db import models
from django.urls import NoReverseMatch, reverse


class SiteSettings(models.Model):
    site_name = models.CharField("nome do site", max_length=80, default="Velurea Clinic")

    whatsapp_number = models.CharField(
        "WhatsApp (só números, com DDI)",
        max_length=20,
        help_text="Usado no link wa.me. Ex.: 905010411230",
    )
    whatsapp_display = models.CharField(
        "WhatsApp (como aparece no site)", max_length=40, help_text="Ex.: +90 501 041 12 30"
    )
    whatsapp_message = models.CharField(
        "mensagem inicial do WhatsApp",
        max_length=200,
        default="Olá! Gostaria de informações sobre tratamentos na Turquia.",
    )
    email = models.EmailField("e-mail de contato")
    address = models.CharField("endereço", max_length=200)
    hours = models.CharField("horário de atendimento", max_length=100)
    languages_label = models.CharField(
        "idiomas (rótulo curto)", max_length=60, default="PT · ES · EN · TR"
    )

    footer_about = models.TextField("texto institucional do rodapé")
    footer_disclaimer = models.CharField(
        "aviso do rodapé",
        max_length=200,
        default="Conteúdo informativo. Não substitui consulta, diagnóstico ou tratamento médico.",
    )

    cta_eyebrow = models.CharField("faixa de chamada — sobretítulo", max_length=80)
    cta_title = models.CharField("faixa de chamada — título", max_length=200)
    cta_text = models.TextField("faixa de chamada — texto")

    lead_notification_email = models.EmailField(
        "enviar novos contatos para",
        blank=True,
        help_text="Cada formulário recebido gera um aviso neste e-mail. "
        "Em branco, usa o e-mail de contato acima.",
    )
    noindex = models.BooleanField(
        "esconder o site do Google",
        default=False,
        help_text="Marque enquanto o site estiver em teste ou demonstração.",
    )

    class Meta:
        verbose_name = "configurações do site"
        verbose_name_plural = "configurações do site"

    def __str__(self):
        return "Configurações do site"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj = cls.objects.filter(pk=1).first()
        return obj or cls(pk=1)

    @property
    def whatsapp_link(self):
        msg = urllib.parse.quote(self.whatsapp_message, safe="!")
        return f"https://wa.me/{self.whatsapp_number}?text={msg}"

    @property
    def notification_email(self):
        return self.lead_notification_email or self.email


class Page(models.Model):
    """Uma página fixa do site. O `key` liga o registro ao template."""

    key = models.SlugField("identificador", max_length=40, unique=True)
    name = models.CharField("página", max_length=80)
    url_name = models.CharField(max_length=60, blank=True)
    order = models.PositiveSmallIntegerField("ordem", default=0)

    seo_title = models.CharField(
        "título na aba / Google", max_length=200, blank=True,
        help_text="Ideal: até 60 caracteres.",
    )
    seo_description = models.CharField(
        "descrição no Google", max_length=300, blank=True,
        help_text="Ideal: até 160 caracteres.",
    )
    og_title = models.CharField(
        "título ao compartilhar", max_length=200, blank=True,
        help_text="WhatsApp, Facebook etc. Em branco, usa o título acima.",
    )
    og_description = models.CharField(
        "descrição ao compartilhar", max_length=300, blank=True,
        help_text="Em branco, usa a descrição acima.",
    )

    cta_title = models.CharField(
        "faixa de chamada — título", max_length=200, blank=True,
        help_text="Em branco, usa o texto padrão das Configurações do site.",
    )
    cta_text = models.TextField(
        "faixa de chamada — texto", blank=True,
        help_text="Em branco, usa o texto padrão das Configurações do site.",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "página"
        verbose_name_plural = "páginas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        try:
            return reverse(self.url_name)
        except NoReverseMatch:
            return "/"

    @property
    def s(self):
        """Seções por chave, para o template: `page.s.hero.title`."""
        if not hasattr(self, "_sections"):
            self._sections = _SectionMap({sec.key: sec for sec in self.sections.all()})
        return self._sections


class _SectionMap(dict):
    """Seção ausente devolve uma seção vazia em vez de quebrar o template."""

    def __missing__(self, key):
        return Section(key=key)


class Section(models.Model):
    """Um bloco de texto de uma página.

    Nem toda seção usa todos os campos: `hint` diz ao cliente quais campos
    aquela seção mostra no site.
    """

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")
    key = models.SlugField("identificador", max_length=40)
    label = models.CharField("seção", max_length=100)
    hint = models.CharField("o que esta seção usa", max_length=300, blank=True)
    used_fields = models.CharField(
        max_length=200, blank=True, editable=False,
        help_text="Campos que o template desta seção exibe, separados por vírgula. "
        "O admin esconde os demais. Vazio = mostra todos.",
    )
    order = models.PositiveSmallIntegerField("ordem", default=0)

    eyebrow = models.CharField(
        "sobretítulo", max_length=150, blank=True,
        help_text="Texto pequeno, em maiúsculas, acima do título.",
    )
    title = models.CharField("título", max_length=250, blank=True)
    text = models.TextField("texto", blank=True)
    body = models.TextField(
        "parágrafos", blank=True,
        help_text="Separe parágrafos com uma linha em branco. "
        "Use **texto** para destacar em negrito.",
    )
    items = models.TextField(
        "lista", blank=True,
        help_text="Um item por linha. Onde houver título e texto, "
        "separe com uma barra vertical: Título | texto.",
    )
    note = models.CharField("texto complementar", max_length=300, blank=True)
    image = models.ImageField(
        "imagem", upload_to="secoes/", blank=True,
        help_text="Em branco, mantém a imagem original do site.",
    )
    image_alt = models.CharField(
        "descrição da imagem", max_length=200, blank=True,
        help_text="Lida por leitores de tela e pelo Google.",
    )

    class Meta:
        ordering = ["page__order", "order"]
        unique_together = [("page", "key")]
        verbose_name = "seção"
        verbose_name_plural = "seções"

    def __str__(self):
        return self.label or self.key

    @property
    def item_list(self):
        return [line.strip() for line in self.items.splitlines() if line.strip()]

    @property
    def item_pairs(self):
        """Linhas no formato `Título | texto`, como lista de (título, texto)."""
        pairs = []
        for line in self.item_list:
            head, _, tail = line.partition("|")
            pairs.append((head.strip(), tail.strip()))
        return pairs


class VisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class OrderedModel(models.Model):
    order = models.PositiveSmallIntegerField("ordem", default=0)
    is_active = models.BooleanField("visível no site", default=True)

    objects = models.Manager()
    visible = VisibleManager()

    class Meta:
        abstract = True
        ordering = ["order", "pk"]


class Step(OrderedModel):
    title = models.CharField("título", max_length=120)
    text = models.TextField("texto")

    class Meta(OrderedModel.Meta):
        verbose_name = "etapa do processo"
        verbose_name_plural = "etapas do processo"

    def __str__(self):
        return self.title


class Differential(OrderedModel):
    title = models.CharField("título", max_length=120)
    text = models.TextField("texto")

    class Meta(OrderedModel.Meta):
        verbose_name = "diferencial"
        verbose_name_plural = "diferenciais"

    def __str__(self):
        return self.title


class Testimonial(OrderedModel):
    name = models.CharField("nome", max_length=100)
    origin = models.CharField("cidade / país", max_length=100)
    treatment = models.CharField("tratamento", max_length=120)
    quote = models.TextField("depoimento")
    on_home = models.BooleanField(
        "mostrar na página inicial", default=False,
        help_text="A página inicial mostra até dois depoimentos.",
    )

    class Meta(OrderedModel.Meta):
        verbose_name = "depoimento"
        verbose_name_plural = "depoimentos"

    def __str__(self):
        return f"{self.name} — {self.treatment}"


class Faq(OrderedModel):
    question = models.CharField("pergunta", max_length=250)
    answer = models.TextField("resposta")

    class Meta(OrderedModel.Meta):
        verbose_name = "pergunta frequente"
        verbose_name_plural = "perguntas frequentes"

    def __str__(self):
        return self.question


class Doctor(OrderedModel):
    name = models.CharField("nome", max_length=120)
    role = models.CharField("especialidade", max_length=150)
    detail = models.TextField("descrição")

    class Meta(OrderedModel.Meta):
        verbose_name = "médico parceiro"
        verbose_name_plural = "médicos parceiros"

    def __str__(self):
        return self.name


class Hospital(OrderedModel):
    name = models.CharField("nome", max_length=150)
    detail = models.TextField("descrição")

    class Meta(OrderedModel.Meta):
        verbose_name = "hospital ou clínica"
        verbose_name_plural = "hospitais e clínicas"

    def __str__(self):
        return self.name
