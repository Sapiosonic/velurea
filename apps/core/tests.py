from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from apps.core.testing import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import Post
from apps.contact.models import Lead
from apps.core.models import Page, Section, SiteSettings
from apps.treatments.models import Treatment

PUBLIC_URLS = [
    "/", "/sobre/", "/tratamentos/", "/tratamentos/oncologia/", "/como-funciona/",
    "/depoimentos/", "/medicos-e-hospitais/", "/blog/", "/perguntas-frequentes/",
    "/contato/", "/obrigado/", "/robots.txt", "/sitemap.xml",
]


class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)

    def test_public_pages_render(self):
        for url in PUBLIC_URLS:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_seed_is_idempotent_and_keeps_edits(self):
        Section.objects.filter(page__key="home", key="hero").update(title="Editado")
        call_command("seed_site", verbosity=0)
        self.assertEqual(Section.objects.get(page__key="home", key="hero").title, "Editado")
        self.assertEqual(Treatment.objects.count(), 10)

    def test_section_edit_shows_on_site(self):
        Section.objects.filter(page__key="sobre", key="hero").update(title="Título novo")
        self.assertContains(self.client.get("/sobre/"), "Título novo")

    def test_settings_change_reaches_every_page(self):
        site = SiteSettings.load()
        site.whatsapp_display = "+90 000 000 00 00"
        site.save()
        for url in ["/", "/contato/", "/tratamentos/odontologia/"]:
            self.assertContains(self.client.get(url), "+90 000 000 00 00")

    def test_hidden_treatment_is_404_and_leaves_footer(self):
        Treatment.objects.filter(slug="oncologia").update(is_active=False)
        self.assertEqual(self.client.get("/tratamentos/oncologia/").status_code, 404)
        self.assertNotContains(self.client.get("/"), "/tratamentos/oncologia/")

    def test_rich_filter_escapes_html(self):
        Section.objects.filter(page__key="contato", key="canais").update(
            body="<script>x</script> **negrito**"
        )
        r = self.client.get("/contato/")
        self.assertNotContains(r, "<script>x</script>")
        self.assertContains(r, '<strong class="text-foreground">negrito</strong>')

    def test_noindex_toggle(self):
        self.assertIn("Disallow: /", self.client.get("/robots.txt").content.decode())
        SiteSettings.objects.filter(pk=1).update(noindex=False)
        self.assertNotContains(self.client.get("/"), "noindex")


class ContactTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)

    def payload(self, **extra):
        dental = Treatment.objects.get(slug_pt_br="odontologia")
        data = {
            "name": "Maria", "email": "maria@example.com", "phone": "+55 11 9",
            "country": "Brasil", "treatment": str(dental.pk), "message": "Oi",
        }
        data.update(extra)
        return data

    def test_valid_submission_saves_and_notifies(self):
        r = self.client.post("/contato/", self.payload())
        self.assertRedirects(r, "/obrigado/")
        lead = Lead.objects.get()
        self.assertEqual(lead.treatment, "Tratamentos Odontológicos")
        self.assertEqual(lead.treatment_ref.slug, "odontologia")
        self.assertEqual(lead.language, "pt-br")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Maria", mail.outbox[0].subject)

    def test_other_procedure(self):
        self.client.post("/contato/", self.payload(treatment="outro"))
        lead = Lead.objects.get()
        self.assertEqual(lead.treatment, "Outro procedimento")
        self.assertIsNone(lead.treatment_ref)

    def test_spanish_form_records_language_and_portuguese_treatment(self):
        SiteSettings.objects.filter(pk=1).update(published_languages="es")
        Treatment.objects.filter(slug="odontologia").update(title_es="Tratamientos dentales")
        r = self.client.get("/es/contacto/")
        self.assertContains(r, "Tratamientos dentales")
        r = self.client.post("/es/contacto/", self.payload())
        self.assertRedirects(r, "/es/gracias/")
        lead = Lead.objects.get()
        self.assertEqual(lead.language, "es")
        self.assertEqual(lead.treatment, "Tratamentos Odontológicos")  # equipe lê em PT
        self.assertIn("[ES]", mail.outbox[0].subject)

    def test_honeypot_is_dropped_silently(self):
        r = self.client.post("/contato/", self.payload(botcheck="sou robô"))
        self.assertRedirects(r, "/obrigado/")
        self.assertEqual(Lead.objects.count(), 0)

    def test_invalid_submission_shows_errors_and_keeps_values(self):
        r = self.client.post("/contato/", self.payload(email="nao-e-email", treatment="X"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "field-error")
        self.assertContains(r, 'value="Maria"')
        self.assertEqual(Lead.objects.count(), 0)


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)

    def test_every_seeded_post_has_a_page(self):
        r = self.client.get("/blog/")
        for post in Post.objects.all():
            with self.subTest(slug=post.slug):
                self.assertContains(r, f'href="{post.get_absolute_url()}"')
                page = self.client.get(post.get_absolute_url())
                self.assertEqual(page.status_code, 200)
                self.assertContains(page, post.title)
                self.assertContains(page, "<h2>")  # o corpo do artigo está lá

    def test_seed_fills_empty_bodies_but_keeps_edited_ones(self):
        Post.objects.filter(slug="fue-ou-dhi").update(body="")
        Post.objects.filter(slug="sleeve-gastrico-turquia").update(body="<p>Editado</p>")
        call_command("seed_site", verbosity=0)
        self.assertIn("Sapphire", Post.objects.get(slug="fue-ou-dhi").body)
        self.assertEqual(Post.objects.get(slug="sleeve-gastrico-turquia").body, "<p>Editado</p>")

    def test_pagination_eight_per_page(self):
        for i in range(17):  # 4 do seed + 17 = 21 → páginas de 8, 8 e 5
            Post.objects.create(
                title=f"Extra {i:02d}", slug=f"extra-{i:02d}", excerpt="e", body="<p>t</p>",
                status=Post.Status.PUBLISHED,
                published_at=timezone.now() - timezone.timedelta(minutes=i),
            )
        counts = []
        for n in (1, 2, 3):
            r = self.client.get("/blog/", {"pagina": n})
            counts.append(len(r.context["posts"].object_list))
        self.assertEqual(counts, [8, 8, 5])

        r = self.client.get("/blog/")
        self.assertContains(r, 'aria-current="page">1<')
        self.assertContains(r, 'href="?pagina=2"')
        self.assertContains(r, 'rel="next"')
        self.assertNotContains(r, 'rel="prev"')

        r = self.client.get("/blog/", {"pagina": 3})
        self.assertContains(r, "<title>Página 3 — ")
        self.assertContains(r, 'rel="canonical" href="http://testserver/blog/?pagina=3"')
        self.assertNotContains(r, 'rel="next"')
        # Link para a página 1 é o endereço limpo, sem ?pagina=1.
        self.assertContains(r, 'href="/blog/" aria-label="Página 1"')

        # Página inválida ou além do fim não quebra.
        self.assertEqual(self.client.get("/blog/", {"pagina": "abc"}).status_code, 200)
        self.assertEqual(self.client.get("/blog/", {"pagina": 99}).context["posts"].number, 3)

    def test_few_posts_have_no_pager(self):
        self.assertNotContains(self.client.get("/blog/"), 'class="pager"')

    def test_post_body_is_sanitized(self):
        post = Post.objects.get(slug="fue-ou-dhi")
        post.body = '<p>Texto <strong>real</strong></p><script>alert(1)</script><a href="x" onclick="y">l</a>'
        post.save()
        r = self.client.get("/blog/fue-ou-dhi/")
        self.assertContains(r, "<strong>real</strong>")
        self.assertNotContains(r, "alert(1)")
        self.assertNotContains(r, "onclick")

    def test_draft_and_scheduled_posts_are_hidden(self):
        draft = Post.objects.create(title="Rascunho", slug="rascunho", excerpt="r",
                                    body="<p>texto</p>", status=Post.Status.DRAFT)
        future = Post.objects.create(title="Futuro", slug="futuro", excerpt="f",
                                     body="<p>texto</p>", status=Post.Status.PUBLISHED,
                                     published_at=timezone.now() + timezone.timedelta(days=3))
        r = self.client.get("/blog/")
        self.assertNotContains(r, "Rascunho")
        self.assertNotContains(r, "Futuro")
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(future.get_absolute_url()).status_code, 404)

        staff = get_user_model().objects.create_user("ed", password="x", is_staff=True)
        self.client.force_login(staff)
        self.assertContains(self.client.get(draft.get_absolute_url()), "Pré-visualização")


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)
        cls.admin = get_user_model().objects.create_superuser("admin", "a@example.com", "x")

    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_every_admin_changelist_and_form_loads(self):
        from django.contrib import admin

        for model, model_admin in admin.site._registry.items():
            info = (model._meta.app_label, model._meta.model_name)
            with self.subTest(model=info):
                r = self.client.get(reverse("admin:%s_%s_changelist" % info), follow=True)
                self.assertEqual(r.status_code, 200)
                obj = model.objects.first()
                if obj:
                    r = self.client.get(reverse("admin:%s_%s_change" % info, args=[obj.pk]))
                    self.assertEqual(r.status_code, 200)

    def test_dashboard_shows_summary_and_theme(self):
        Lead.objects.create(name="Ana", email="ana@example.com", phone="1", country="BR",
                            treatment="Odontologia", message="Oi")
        r = self.client.get(reverse("admin:index"))
        self.assertContains(r, "admin-theme/velurea-admin.css")
        self.assertContains(r, "Olá, admin.")
        self.assertContains(r, "Contatos novos")
        self.assertContains(r, reverse("admin:contact_lead_changelist") + "?status__exact=new")
        self.assertContains(r, reverse("admin:blog_post_add"))
        # A lista original de seções do admin continua lá.
        self.assertContains(r, reverse("admin:core_page_changelist"))

    def test_dashboard_respects_permissions(self):
        staff = get_user_model().objects.create_user("ed", password="x", is_staff=True)
        self.client.force_login(staff)
        r = self.client.get(reverse("admin:index"))
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "Contatos novos")
        self.assertNotContains(r, "Novo post")

    def test_pages_cannot_be_added_or_deleted(self):
        page = Page.objects.get(key="home")
        self.assertEqual(self.client.get(reverse("admin:core_page_add")).status_code, 403)
        self.assertEqual(
            self.client.get(reverse("admin:core_page_delete", args=[page.pk])).status_code, 403
        )

    def _page_post_data(self, page, section_edits):
        """Dados do formulário do admin da página, campo a campo por idioma."""
        sfx = [code.replace("-", "_") for code, _ in settings.LANGUAGES]
        sections = list(page.sections.all())
        data = {
            "sections-TOTAL_FORMS": len(sections), "sections-INITIAL_FORMS": len(sections),
            "sections-MIN_NUM_FORMS": 0, "sections-MAX_NUM_FORMS": 1000,
        }
        for f in ["seo_title", "seo_description", "og_title", "og_description", "cta_title", "cta_text"]:
            for s in sfx:
                data[f"{f}_{s}"] = getattr(page, f"{f}_{s}") or ""
        for i, sec in enumerate(sections):
            data[f"sections-{i}-id"] = sec.pk
            data[f"sections-{i}-page"] = page.pk
            for f in ["eyebrow", "title", "text", "body", "items", "note", "image_alt"]:
                for s in sfx:
                    key = f"{f}_{s}"
                    data[f"sections-{i}-{key}"] = section_edits.get((sec.key, key), getattr(sec, key) or "")
        return data

    def test_section_edit_through_admin(self):
        page = Page.objects.get(key="faq")
        url = reverse("admin:core_page_change", args=[page.pk])
        data = self._page_post_data(page, {
            ("hero", "title_pt_br"): "Dúvidas",
            ("hero", "title_es"): "Preguntas frecuentes",
        })
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, 302, getattr(r, "context", None) and r.context["errors"])
        self.client.logout()
        self.assertContains(self.client.get("/perguntas-frequentes/"), "Dúvidas")
        # Espanhol ainda não publicado: o público não vê.
        self.assertEqual(self.client.get("/es/preguntas-frecuentes/").status_code, 404)
        SiteSettings.objects.filter(pk=1).update(published_languages="es")
        self.assertContains(self.client.get("/es/preguntas-frecuentes/"), "Preguntas frecuentes")

    def test_admin_has_language_tabs(self):
        page = Page.objects.get(key="home")
        r = self.client.get(reverse("admin:core_page_change", args=[page.pk]))
        for name in ["title_pt_br", "title_es", "title_en", "title_tr"]:
            self.assertContains(r, f"-{name}")

    def test_published_languages_checkboxes(self):
        url = reverse("admin:core_sitesettings_change", args=[1])
        r = self.client.get(url)
        self.assertContains(r, 'name="published" value="es"')
        self.assertNotContains(r, 'name="published" value="pt-br"')
