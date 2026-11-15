from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render

from apps.core import languages
from apps.core.views import get_page

from .models import Category, Post

PER_PAGE = 8


def post_list(request, category_slug=None):
    posts = Post.published.for_language(languages.current())
    category = None
    if category_slug:
        category, should_redirect = languages.find_by_slug(Category.objects.all(), category_slug)
        if category is None:
            raise Http404
        if should_redirect:
            return redirect("blog:category", category_slug=category.slug, permanent=True)
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
    lang = languages.current()
    post, should_redirect = languages.find_by_slug(Post.objects.select_related("category"), slug)
    if post is None:
        raise Http404

    # Quem está logado no admin vê rascunhos e posts ainda sem tradução
    # (com o texto em português no lugar), para revisar antes de publicar.
    if not request.user.is_staff:
        if not post.is_live or not post.is_translated(lang):
            raise Http404
    if should_redirect:
        return redirect(post, permanent=True)

    # "Leia também": primeiro da mesma categoria, completando com os mais recentes.
    others = Post.published.for_language(lang).exclude(pk=post.pk)
    related = list(others.filter(category_id=post.category_id)[:2]) if post.category_id else []
    if len(related) < 2:
        related += list(others.exclude(pk__in=[p.pk for p in related])[: 2 - len(related)])

    # O post só tem versão nos idiomas em que foi traduzido.
    translated_in = [code for code in request.published_languages if post.is_translated(code)]
    return render(
        request, "blog/detail.html",
        {
            "post": post,
            "related": related,
            "alternates": languages.alternates_for_object(post, translated_in),
        },
    )
