from django import forms
from .models import Risposta


class EmailForm(forms.Form):
    email = forms.EmailField(
        label="La sua email",
        widget=forms.EmailInput(attrs={"placeholder": "nome@esempio.it", "autofocus": True}),
    )


class RispostaForm(forms.ModelForm):
    # Q6 ammette più risposte: checkbox al posto dei radio
    q6_proposta = forms.MultipleChoiceField(
        choices=Risposta.Proposta.choices,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Risposta
        fields = [
            "q1_giro_affari",
            "q2_misura_dannosa",
            "q3_impatto_parcheggi",
            "q4_impatto_via_mazzini",
            "q5_frequenza_residenti",
            "q6_proposta",
            "q7_note",
            "q8_tipo_attivita",
            "q9_posizione",
            "q10_contatto_disponibile",
            "q10_recapito",
        ]
        widgets = {
            "q1_giro_affari": forms.RadioSelect,
            "q2_misura_dannosa": forms.RadioSelect,
            "q3_impatto_parcheggi": forms.RadioSelect,
            "q4_impatto_via_mazzini": forms.RadioSelect,
            "q5_frequenza_residenti": forms.RadioSelect,
            "q7_note": forms.Textarea(attrs={"rows": 4, "placeholder": "Scrivi qui eventuali proposte o segnalazioni…"}),
            "q8_tipo_attivita": forms.RadioSelect,
            "q9_posizione": forms.RadioSelect,
            "q10_contatto_disponibile": forms.RadioSelect,
            "q10_recapito": forms.TextInput(attrs={"placeholder": "Telefono o email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field, "choices"):
                field.choices = [(v, l) for v, l in field.choices if v != ""]

    def clean(self):
        cleaned = super().clean()
        disponibile = cleaned.get("q10_contatto_disponibile")
        recapito = cleaned.get("q10_recapito", "").strip()
        if disponibile == Risposta.DisponibileContatto.SI and not recapito:
            self.add_error("q10_recapito", "Inserisci un recapito se sei disponibile a essere ricontattato.")
        return cleaned
