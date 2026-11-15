from django import forms

from apps.treatments.models import Treatment

from .models import Lead

OTHER = "Outro procedimento"


class LeadForm(forms.ModelForm):
    # Honeypot: invisível para pessoas, preenchido por robôs que completam
    # todos os campos. Envio com ele marcado é descartado em silêncio.
    botcheck = forms.CharField(required=False)

    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "country", "treatment", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        titles = list(Treatment.visible.values_list("title", flat=True))
        self.treatment_choices = titles + [OTHER]
        self.fields["message"].required = False

    def clean_treatment(self):
        value = self.cleaned_data["treatment"]
        if value not in self.treatment_choices:
            raise forms.ValidationError("Selecione um tratamento da lista.")
        return value

    @property
    def is_spam(self):
        return bool(self.cleaned_data.get("botcheck"))
