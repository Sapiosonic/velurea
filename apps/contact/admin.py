from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["name", "treatment", "language", "country", "email", "phone", "status", "created_at"]
    list_filter = ["status", "language", "treatment", "created_at"]
    list_editable = ["status"]
    search_fields = ["name", "email", "phone", "message"]
    date_hierarchy = "created_at"
    readonly_fields = [
        "name", "email", "phone", "country", "treatment", "treatment_ref", "language", "message",
        "created_at", "ip_address",
    ]
    fieldsets = [
        ("Solicitação", {"fields": [
            "name", "email", "phone", "country", "language", "treatment", "message",
            "created_at",
        ]}),
        ("Atendimento", {"fields": ["status", "notes"]}),
        ("Técnico", {"fields": ["treatment_ref", "ip_address"], "classes": ["collapse"]}),
    ]

    def has_add_permission(self, request):
        return False
