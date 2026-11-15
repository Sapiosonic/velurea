"""Internacionalização: rotas por idioma, publicação, seletor, hreflang e slugs."""

from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.core.testing import TestCase

from apps.blog.models import Post
from apps.core.models import SiteSettings
from apps.treatments.models import Treatment


def publish(*codes):
    SiteSettings.objects.filter(pk=1).update(published_languages=",".join(codes))


class LanguageRoutingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)

    def test_portuguese_has_no_prefix_and_ignores_browser_language(self):
        r = self.client.get("/contato/", HTTP_ACCEPT_LANGUAGE="es")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '<html lang="pt-BR">')
        self.assertContains(r, "Nome completo")

    def test_unpublished_language_is_404_for_public(self):
        for url in ["/es/", "/en/contact/", "/tr/tedaviler/"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_staff_previews_unpublished_language_with_portuguese_fallback(self):
        staff = get_user_model().objects.create_user("ed", password="x", is_staff=True)
        self.client.force_login(staff)
        r = self.client.get("/es/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '<html lang="es">')
        self.assertContains(r, "lang-preview-bar")
        self.assertContains(r, "noindex")
        # Sem tradução ainda: o conteúdo aparece em português.
        self.assertContains(r, "Sua jornada médica na Turquia")

    def test_published_language_is_public(self):
        publish("es")
        r = self.client.get("/es/contacto/")
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "lang-preview-bar")
        self.assertEqual(self.client.get("/en/contact/").status_code, 404)

    def test_admin_stays_in_portuguese(self):
        admin = get_user_model().objects.create_superuser("a", "a@example.com", "x")
        self.client.force_login(admin)
        r = self.client.get("/admin/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertContains(r, "Configurações do site")


class SwitcherAndSeoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)

    def test_only_portuguese_keeps_original_footer_and_no_hreflang(self):
        r = self.client.get("/")
        self.assertContains(r, "PT · ES · EN · TR")
        self.assertNotContains(r, "hreflang")
        self.assertNotContains(r, "lang-switch")

    def test_switcher_and_hreflang_point_to_same_page(self):
        publish("es", "en")
        r = self.client.get("/perguntas-frequentes/")
        self.assertContains(r, '<details class="lang-menu">')
        self.assertContains(r, 'href="/es/preguntas-frecuentes/"')
        self.assertContains(r, 'href="/en/faq/"')
        self.assertNotContains(r, "/tr/")  # turco não publicado
        self.assertContains(r, '<link rel="alternate" hreflang="pt-BR" href="http://testserver/perguntas-frequentes/">')
        self.assertContains(r, '<link rel="alternate" hreflang="es" href="http://testserver/es/preguntas-frecuentes/">')
        self.assertContains(r, 'hreflang="x-default" href="http://testserver/perguntas-frequentes/"')

    def test_sitemap_lists_published_languages_with_alternates(self):
        publish("es")
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("http://testserver/es/contacto/", xml)
        self.assertIn('hreflang="pt-br"', xml)
        self.assertNotIn("/en/", xml)

    def test_dates_follow_language(self):
        publish("en")
        Post.objects.filter(slug="fue-ou-dhi").update(title_en="FUE or DHI", excerpt_en="x", body_en="<p>x</p>",
                                                      slug_en="fue-or-dhi")
        self.assertContains(self.client.get("/blog/fue-ou-dhi/"), "27 de fevereiro de 2026")
        self.assertContains(self.client.get("/en/blog/fue-or-dhi/"), "February 27, 2026")


class TranslatedSlugTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)
        publish("es")

    def test_translated_treatment_slug_and_redirect_from_portuguese_slug(self):
        Treatment.objects.filter(slug="odontologia").update(
            slug_es="odontologia-dental", title_es="Tratamientos dentales")
        r = self.client.get("/es/tratamientos/odontologia-dental/")
        self.assertContains(r, "Tratamientos dentales")
        r = self.client.get("/es/tratamientos/odontologia/")
        self.assertRedirects(r, "/es/tratamientos/odontologia-dental/", status_code=301)
        # Português continua no endereço de sempre.
        self.assertContains(self.client.get("/tratamentos/odontologia/"), "Tratamentos Odontológicos")

    def test_untranslated_treatment_uses_portuguese_slug(self):
        r = self.client.get("/es/tratamientos/oncologia/")
        self.assertEqual(r.status_code, 200)

    def test_blog_shows_only_posts_translated_into_the_language(self):
        r = self.client.get("/es/blog/")
        self.assertContains(r, "Nenhum artigo publicado ainda.")  # texto fixo ainda sem tradução
        self.assertEqual(self.client.get("/es/blog/fue-ou-dhi/").status_code, 404)

        Post.objects.filter(slug_pt_br="fue-ou-dhi").update(
            title_es="FUE o DHI", slug_es="fue-o-dhi", excerpt_es="Resumen", body_es="<p>Texto</p>")
        r = self.client.get("/es/blog/")
        self.assertContains(r, "FUE o DHI")
        self.assertNotContains(r, "Sleeve gástrico")
        self.assertContains(self.client.get("/es/blog/fue-o-dhi/"), "Texto")

    def test_post_hreflang_only_lists_translated_versions(self):
        r = self.client.get("/blog/fue-ou-dhi/")
        self.assertNotContains(r, 'hreflang="es"')
        Post.objects.filter(slug="fue-ou-dhi").update(title_es="FUE o DHI", slug_es="fue-o-dhi")
        r = self.client.get("/blog/fue-ou-dhi/")
        self.assertContains(r, 'hreflang="es" href="http://testserver/es/blog/fue-o-dhi/"')

    def test_body_sanitized_in_every_language(self):
        post = Post.objects.get(slug="fue-ou-dhi")
        post.body_es = "<p>ok</p><script>alert(1)</script>"
        post.save()
        post.refresh_from_db()
        self.assertNotIn("script", post.body_es)
