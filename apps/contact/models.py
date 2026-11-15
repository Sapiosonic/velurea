from django.conf import settings
from django.db import models


class Lead(models.Model):
    """Uma solicitação de avaliação enviada pelo formulário de contato."""

    class Status(models.TextChoices):
        NEW = "new", "Novo"
        IN_PROGRESS = "in_progress", "Em atendimento"
        DONE = "done", "Concluído"
        DISCARDED = "discarded", "Descartado"

    name = models.CharField("nome", max_length=150)
    email = models.EmailField("e-mail")
    phone = models.CharField("WhatsApp", max_length=40)
    country = models.CharField("país", max_length=80)
    treatment = models.CharField("tratamento de interesse", max_length=150)
    treatment_ref = models.ForeignKey(
        "treatments.Treatment", verbose_name="tratamento (cadastro)",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="leads",
    )
    language = models.CharField(
        "idioma do contato", max_length=10, choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        help_text="Idioma em que o paciente preencheu o formulário — responda nele.",
    )
    message = models.TextField("mensagem", blank=True)

    status = models.CharField(
        "situação", max_length=12, choices=Status.choices, default=Status.NEW
    )
    notes = models.TextField("anotações internas", blank=True)

    created_at = models.DateTimeField("recebido em", auto_now_add=True)
    ip_address = models.GenericIPAddressField("IP", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contato recebido"
        verbose_name_plural = "contatos recebidos"

    def __str__(self):
        return f"{self.name} — {self.treatment}"
