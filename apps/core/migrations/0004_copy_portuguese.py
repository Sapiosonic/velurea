"""Copia o conteúdo existente para as colunas em português.

Ao ativar o modeltranslation, cada campo traduzível ganhou colunas por idioma
(title_pt_br, title_es…), todas vazias. O texto já cadastrado continua na
coluna original; aqui ele é copiado para a coluna do português, que passa a
ser a fonte do site. Os outros idiomas ficam vazios, para os tradutores.

Lista congelada de propósito: migrations não devem importar translation.py,
que muda com o tempo.
"""

from django.db import migrations

FIELDS = {
    ("core", "SiteSettings"): ["whatsapp_message", "address", "hours", "footer_about",
                               "footer_disclaimer", "cta_eyebrow", "cta_title", "cta_text"],
    ("core", "Page"): ["seo_title", "seo_description", "og_title", "og_description",
                       "cta_title", "cta_text"],
    ("core", "Section"): ["eyebrow", "title", "text", "body", "items", "note", "image_alt"],
    ("core", "Step"): ["title", "text"],
    ("core", "Differential"): ["title", "text"],
    ("core", "Testimonial"): ["treatment"],
    ("core", "Faq"): ["question", "answer"],
    ("core", "Doctor"): ["role", "detail"],
    ("core", "Hospital"): ["name", "detail"],
    ("treatments", "Treatment"): ["slug", "title", "short", "intro", "procedures", "areas",
                                  "duration", "stay", "includes", "candidates", "seo_title"],
    ("blog", "Category"): ["name", "slug"],
    ("blog", "Post"): ["title", "slug", "excerpt", "body", "cover_alt", "seo_title"],
}


def copy_to_portuguese(apps, schema_editor):
    for (app_label, model_name), fields in FIELDS.items():
        model = apps.get_model(app_label, model_name)
        for obj in model.objects.all():
            changed = []
            for field in fields:
                target = f"{field}_pt_br"
                if not getattr(obj, target):
                    setattr(obj, target, getattr(obj, field))
                    changed.append(target)
            if changed:
                obj.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_translations"),
        ("treatments", "0002_translations"),
        ("blog", "0002_translations"),
    ]

    operations = [migrations.RunPython(copy_to_portuguese, migrations.RunPython.noop)]
