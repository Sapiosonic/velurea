from django.http import Http404
from django.shortcuts import redirect, render

from apps.core import languages
from apps.core.views import get_page

from .models import Treatment


def treatment_list(request):
    return render(
        request, "treatments/list.html",
        {"page": get_page("tratamentos"), "treatments": Treatment.visible.all()},
    )


def treatment_detail(request, slug):
    treatment, should_redirect = languages.find_by_slug(Treatment.visible.all(), slug)
    if treatment is None:
        raise Http404
    if should_redirect:
        return redirect(treatment, permanent=True)

    others = Treatment.visible.exclude(pk=treatment.pk)
    return render(
        request, "treatments/detail.html",
        {
            "treatment": treatment,
            "others": others,
            "alternates": languages.alternates_for_object(treatment, request.published_languages),
        },
    )
