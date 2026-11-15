from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.core import languages
from apps.treatments.models import Treatment

from .models import Lead

OTHER = "outro"
OTHER_LABEL_PT = "Outro procedimento"


class LeadForm(forms.ModelForm):
    # Honeypot: invisível para pessoas, preenchido por robôs que completam
    # todos os campos. Envio com ele marcado é descartado em silêncio.
    botcheck = forms.CharField(required=False)

    # O visitante escolhe pelo nome no idioma dele; o formulário envia o id.
    # Assim o contato aponta para o tratamento certo em qualquer idioma.
    treatment = forms.ChoiceField(
        error_messages={
            "required": _("Selecione um tratamento da lista."),
            "invalid_choice": _("Selecione um tratamento da lista."),
        },
    )

    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "country", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.treatments = {str(t.pk): t for t in Treatment.visible.all()}
        self.treatment_choices = [(pk, t.title) for pk, t in self.treatments.items()]
        self.treatment_choices.append((OTHER, _("Outro procedimento")))
        self.fields["treatment"].choices = self.treatment_choices
        self.fields["message"].required = False

    def save(self, commit=True):
        lead = super().save(commit=False)
        lead.language = languages.current()
        treatment = self.treatments.get(self.cleaned_data["treatment"])
        lead.treatment_ref = treatment
        # O nome gravado fica sempre em português: é o idioma da equipe que
        # atende, qualquer que seja o idioma em que o paciente escreveu.
        with translation.override(settings.LANGUAGE_CODE):
            lead.treatment = treatment.title if treatment else OTHER_LABEL_PT
        if commit:
            lead.save()
        return lead

    @property
    def is_spam(self):
        return bool(self.cleaned_data.get("botcheck"))
