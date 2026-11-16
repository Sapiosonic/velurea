"""Internacionalização: rotas por idioma, publicação, seletor, hreflang e slugs."""

from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.core.testing import TestCase

from apps.blog.models import Post
from apps.core.models import Page, Section, SiteSettings
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
        # Campo sem tradução no idioma: aparece em português.
        Section.objects.filter(page__key="home", key="hero").update(title_tr="")
        r = self.client.get("/tr/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '<html lang="tr">')
        self.assertContains(r, "lang-preview-bar")
        self.assertContains(r, "noindex")
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
        publish("es", "en", "tr")

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
        # Sem nenhum post traduzido para o turco:
        Post.objects.update(title_tr="")
        r = self.client.get("/tr/blog/")
        self.assertContains(r, "Henüz yayımlanmış yazı yok.")
        self.assertEqual(self.client.get("/tr/blog/fue-mi-dhi-mi/").status_code, 404)

        Post.objects.filter(slug_pt_br="fue-ou-dhi").update(
            title_tr="FUE mi DHI mi", slug_tr="fue-mi-dhi-mi", excerpt_tr="Özet", body_tr="<p>Metin</p>")
        r = self.client.get("/tr/blog/")
        self.assertContains(r, "FUE mi DHI mi")
        self.assertNotContains(r, "Sleeve gástrico")
        self.assertContains(self.client.get("/tr/blog/fue-mi-dhi-mi/"), "Metin")

    def test_post_hreflang_only_lists_translated_versions(self):
        Post.objects.filter(slug_pt_br="fue-ou-dhi").update(title_tr="", slug_tr=None)
        r = self.client.get("/blog/fue-ou-dhi/")
        self.assertContains(r, 'hreflang="es" href="http://testserver/es/blog/fue-o-dhi/"')
        self.assertContains(r, 'hreflang="en" href="http://testserver/en/blog/fue-or-dhi/"')
        self.assertNotContains(r, 'hreflang="tr"')
        Post.objects.filter(slug_pt_br="fue-ou-dhi").update(title_tr="FUE mi DHI mi", slug_tr="fue-mi-dhi-mi")
        r = self.client.get("/blog/fue-ou-dhi/")
        self.assertContains(r, 'hreflang="tr" href="http://testserver/tr/blog/fue-mi-dhi-mi/"')

    def test_body_sanitized_in_every_language(self):
        post = Post.objects.get(slug_pt_br="fue-ou-dhi")
        post.body_es = "<p>ok</p><script>alert(1)</script>"
        post.save()
        post.refresh_from_db()
        self.assertNotIn("script", post.body_es)


class SpanishContentTests(TestCase):
    """Fases 2 a 4: as traduções vêm de locale/content/<idioma>.json."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)
        publish("es")

    def test_translation_file_matches_seeded_content(self):
        from apps.core import content_translations

        # Toda chave do arquivo aponta para um registro existente e todo campo
        # com texto em português tem tradução.
        for lang in ("es", "en", "tr"):
            with self.subTest(lang=lang):
                result = content_translations.apply(lang, content_translations.load_file(lang))
                self.assertEqual(result["missing"], 0)
                done, total = content_translations.overview(lang)
                self.assertEqual(done, total)

    def test_spanish_pages_render_translated_content_and_ui(self):
        r = self.client.get("/es/")
        self.assertContains(r, "Tu recorrido médico en Turquía")
        self.assertContains(r, "Evaluación gratuita")  # texto fixo (django.po)
        self.assertNotContains(r, "Sua jornada médica")
        r = self.client.get("/es/contacto/")
        self.assertContains(r, "Nombre completo")
        self.assertContains(r, "Otro procedimiento")

    def test_spanish_slugs_and_internal_links(self):
        self.assertContains(self.client.get("/es/tratamientos/celulas-madre/"), "Células Madre")
        r = self.client.get("/es/blog/manga-gastrica-turquia/")
        self.assertContains(r, 'href="/es/contacto/"')
        self.assertContains(self.client.get("/es/blog/"), "Leer artículo", count=4)

    def test_site_settings_defaults_are_translated(self):
        # Campos com valor padrão nascem com o português copiado em todas as
        # colunas; a importação trata isso como "não traduzido".
        site = SiteSettings.objects.get(pk=1)
        self.assertTrue(site.whatsapp_message_es.startswith("¡Hola!"))

    def test_import_never_overwrites_admin_edits(self):
        from apps.core import content_translations

        Treatment.objects.filter(slug_pt_br="oncologia").update(title_es="Editado no admin")
        content_translations.apply("es", content_translations.load_file("es"))
        self.assertEqual(Treatment.objects.get(slug_pt_br="oncologia").title_es, "Editado no admin")
        content_translations.apply("es", content_translations.load_file("es"), overwrite=True)
        self.assertEqual(Treatment.objects.get(slug_pt_br="oncologia").title_es, "Oncología y Cirugía Oncológica")

    def test_admin_shows_translation_status(self):
        admin = get_user_model().objects.create_superuser("a", "a@example.com", "x")
        self.client.force_login(admin)
        r = self.client.get("/admin/core/page/")
        self.assertContains(r, "ES ✓")
        self.assertContains(r, "EN ✓")
        self.assertContains(r, "TR ✓")
        # Um campo apagado vira "parcial" na lista.
        Page.objects.filter(key="faq").update(seo_title_tr="")
        r = self.client.get("/admin/core/page/")
        self.assertRegex(r.content.decode(), r"TR \d+/\d+")
        r = self.client.get("/admin/core/sitesettings/1/change/")
        self.assertContains(r, "Situação das traduções")
        self.assertContains(r, "100%")


class EnglishContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)
        publish("es", "en")

    def test_english_pages_render_translated_content_and_ui(self):
        r = self.client.get("/en/")
        self.assertContains(r, "Your medical journey in Turkey")
        self.assertContains(r, "Free assessment")
        r = self.client.get("/en/contact/")
        self.assertContains(r, "Full name")
        self.assertContains(r, "Other procedure")

    def test_english_slugs_switcher_and_internal_links(self):
        r = self.client.get("/en/treatments/plastic-surgery/")
        self.assertContains(r, "Facial and Body Plastic Surgery")
        self.assertContains(r, 'href="/es/tratamientos/cirugia-plastica/"')
        self.assertContains(r, 'href="/tratamentos/cirurgia-plastica/"')
        r = self.client.get("/en/blog/gastric-sleeve-turkey/")
        self.assertContains(r, 'href="/en/contact/"')
        self.assertContains(self.client.get("/en/blog/category/hair-transplant/"), "FUE or DHI")


class TurkishContentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", verbosity=0)
        publish("es", "en", "tr")

    def test_turkish_pages_render_translated_content_and_ui(self):
        r = self.client.get("/tr/")
        self.assertContains(r, '<html lang="tr">')
        self.assertContains(r, "Türkiye&#x27;deki tedavi süreciniz")
        self.assertContains(r, "Ücretsiz değerlendirme")
        r = self.client.get("/tr/iletisim/")
        self.assertContains(r, "Ad soyad")
        self.assertContains(r, "Başka bir işlem")

    def test_turkish_slugs_and_internal_links(self):
        self.assertContains(self.client.get("/tr/tedaviler/ortopedi-boy-uzatma/"), "Boy Uzatma")
        r = self.client.get("/tr/blog/turkiyede-tup-mide/")
        self.assertContains(r, 'href="/tr/iletisim/"')
        self.assertContains(self.client.get("/tr/blog/kategori/sac-ekimi/"), "FUE mi DHI mı")
