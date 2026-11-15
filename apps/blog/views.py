from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from apps.core.views import get_page

from .models import Category, Post

PER_PAGE = 8


def post_list(request, category_slug=None):
    posts = Post.published.all()
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, PER_PAGE)
    # get_page tolera ?pagina=abc ou ?pagina=999: cai na primeira/última página.
    page_obj = paginator.get_page(request.GET.get("pagina"))
    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)
    return render(
        request, "blog/list.html",
        {
            "page": get_page("blog"),
            "posts": page_obj,
            "page_range": page_range,
            "category": category,
            "ellipsis": Paginator.ELLIPSIS,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("category"), slug=slug)
    # Quem está logado no admin vê o rascunho, para revisar antes de publicar.
    if not post.is_live and not request.user.is_staff:
        raise Http404

    # "Leia também": primeiro da mesma categoria, completando com os mais recentes.
    others = Post.published.exclude(pk=post.pk)
    related = list(others.filter(category_id=post.category_id)[:2]) if post.category_id else []
    if len(related) < 2:
        related += list(others.exclude(pk__in=[p.pk for p in related])[: 2 - len(related)])

    return render(request, "blog/detail.html", {"post": post, "related": related})
