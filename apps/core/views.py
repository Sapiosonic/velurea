from django.http import HttpResponse
from django.shortcuts import render

from apps.treatments.models import Treatment

from .models import Differential, Doctor, Faq, Hospital, Page, SiteSettings, Step, Testimonial


def get_page(key):
    page = Page.objects.prefetch_related("sections").filter(key=key).first()
    # Antes de rodar `seed_site`, a página ainda não existe no banco; uma
    # página vazia mantém o site de pé em vez de dar erro 500.
    return page or Page(key=key, name=key)


def render_page(request, key, template, **context):
    return render(request, template, {"page": get_page(key), **context})


def home(request):
    testimonials = list(Testimonial.visible.filter(on_home=True)[:2])
    if not testimonials:
        testimonials = list(Testimonial.visible.all()[:2])
    return render_page(
        request, "home", "core/home.html",
        treatments=Treatment.visible.all(),
        steps=Step.visible.all(),
        differentials=Differential.visible.all(),
        testimonials=testimonials,
    )


def sobre(request):
    return render_page(request, "sobre", "core/sobre.html", differentials=Differential.visible.all())


def como_funciona(request):
    return render_page(request, "como-funciona", "core/como_funciona.html", steps=Step.visible.all())


def depoimentos(request):
    return render_page(
        request, "depoimentos", "core/depoimentos.html", testimonials=Testimonial.visible.all()
    )


def medicos(request):
    return render_page(
        request, "medicos", "core/medicos.html",
        doctors=Doctor.visible.all(), hospitals=Hospital.visible.all(),
    )


def faq(request):
    return render_page(request, "faq", "core/faq.html", faqs=Faq.visible.all())


def obrigado(request):
    return render_page(request, "obrigado", "core/obrigado.html")


def robots_txt(request):
    if SiteSettings.load().noindex:
        lines = ["User-agent: *", "Disallow: /"]
    else:
        lines = [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def page_not_found(request, exception=None):
    return render(request, "404.html", status=404)
