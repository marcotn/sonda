from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Risposta
from .views import genera_token


@admin.register(Risposta)
class RispostaAdmin(admin.ModelAdmin):
    list_display = ["pk", "email", "q8_tipo_attivita", "q9_posizione", "q1_giro_affari", "compilato_il"]
    list_filter = ["q1_giro_affari", "q8_tipo_attivita", "q9_posizione", "q10_contatto_disponibile"]
    readonly_fields = ["compilato_il", "link_invito"]
    ordering = ["-compilato_il"]
    actions = ["mostra_link_invito"]

    def link_invito(self, obj):
        if not obj.pk or not obj.email:
            return "—"
        token = genera_token(obj.email)
        url = f"/q/{token}/"
        return format_html('<a href="{url}" target="_blank">{url}</a>', url=url)
    link_invito.short_description = "Link invito personale"

    @admin.action(description="Mostra link di invito per le email selezionate")
    def mostra_link_invito(self, request, queryset):
        righe = []
        for obj in queryset.exclude(email=""):
            token = genera_token(obj.email)
            righe.append(f"{obj.email} → /q/{token}/")
        if righe:
            self.message_user(request, " | ".join(righe), level=messages.INFO)
        else:
            self.message_user(request, "Nessuna email trovata nelle righe selezionate.", level=messages.WARNING)
