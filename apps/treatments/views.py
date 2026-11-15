from django.shortcuts import get_object_or_404, render

from apps.core.views import get_page

from .models import Treatment


def treatment_list(request):
    return render(
        request, "treatments/list.html",
        {"page": get_page("tratamentos"), "treatments": Treatment.visible.all()},
    )


def treatment_detail(request, slug):
    treatment = get_object_or_404(Treatment.visible, slug=slug)
    others = Treatment.visible.exclude(pk=treatment.pk).only("slug", "title")
    return render(
        request, "treatments/detail.html", {"treatment": treatment, "others": others}
    )
