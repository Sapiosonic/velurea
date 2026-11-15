import logging

from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.core.models import SiteSettings
from apps.core.views import get_page

from .forms import LeadForm

log = logging.getLogger(__name__)


def contato(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            if not form.is_spam:
                lead = form.save(commit=False)
                lead.ip_address = request.META.get("REMOTE_ADDR") or None
                lead.save()
                notify(request, lead)
            return redirect("obrigado")
    else:
        form = LeadForm()

    return render(request, "contact/contato.html", {"page": get_page("contato"), "form": form})


def notify(request, lead):
    """Avisa a equipe por e-mail. Falha no envio não perde o contato: ele já
    está salvo e aparece no admin em "Contatos recebidos"."""
    site = SiteSettings.load()
    if not site.notification_email:
        return
    admin_url = request.build_absolute_uri(
        reverse("admin:contact_lead_change", args=[lead.pk])
    )
    body = "\n".join(
        [
            f"Nome: {lead.name}",
            f"E-mail: {lead.email}",
            f"WhatsApp: {lead.phone}",
            f"País: {lead.country}",
            f"Tratamento: {lead.treatment}",
            f"Idioma do formulário: {lead.get_language_display()} — responda neste idioma",
            "",
            "Mensagem:",
            lead.message or "(sem mensagem)",
            "",
            f"Ver no admin: {admin_url}",
        ]
    )
    try:
        send_mail(
            subject=f"Nova solicitação de avaliação [{lead.language.upper()}] — {lead.name}",
            message=body,
            from_email=None,
            recipient_list=[site.notification_email],
        )
    except Exception:
        log.exception("Falha ao enviar aviso do contato %s", lead.pk)
