from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core import signing
from django.db.models import Count
from .forms import EmailForm, RispostaForm
from .models import Risposta

SESSION_EMAIL_KEY = "questionario_email"
TOKEN_SALT = "questionario-invito"


def _decode_token(token):
    try:
        return signing.loads(token, salt=TOKEN_SALT, max_age=60 * 60 * 24 * 30)  # 30 giorni
    except signing.BadSignature:
        return None


def genera_token(email):
    return signing.dumps(email, salt=TOKEN_SALT)


def email_gate(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            request.session[SESSION_EMAIL_KEY] = form.cleaned_data["email"]
            if request.htmx:
                return render(request, "questionario/partials/questionario_step.html", {
                    "form": RispostaForm(),
                })
            return redirect("questionario")
        if request.htmx:
            return render(request, "questionario/partials/email_step.html", {"form": form})
    else:
        form = EmailForm()

    return render(request, "questionario/index.html", {"form": form, "step": "email"})


def questionario(request):
    email = request.session.get(SESSION_EMAIL_KEY)
    if not email:
        return redirect("email_gate")

    if request.method == "POST":
        form = RispostaForm(request.POST)
        if form.is_valid():
            risposta = form.save(commit=False)
            risposta.email = email
            risposta.save()
            del request.session[SESSION_EMAIL_KEY]
            if request.htmx:
                return render(request, "questionario/grazie.html")
            return redirect("grazie")
        if request.htmx:
            return render(request, "questionario/partials/form_body.html", {"form": form})
    else:
        form = RispostaForm()

    return render(request, "questionario/index.html", {"form": form, "step": "questionario"})


def questionario_invito(request, token):
    email = _decode_token(token)
    if not email:
        return render(request, "questionario/link_non_valido.html", status=400)

    esistente = Risposta.objects.filter(email=email).order_by("-compilato_il").first()

    if request.method == "POST":
        form = RispostaForm(request.POST, instance=esistente)
        if form.is_valid():
            risposta = form.save(commit=False)
            risposta.email = email
            risposta.save()
            if request.htmx:
                return render(request, "questionario/grazie.html")
            return redirect("grazie")
        if request.htmx:
            return render(request, "questionario/partials/form_body.html", {"form": form, "token": token})
    else:
        form = RispostaForm(instance=esistente)

    return render(request, "questionario/index.html", {
        "form": form,
        "step": "questionario",
        "token": token,
        "gia_compilato": esistente is not None,
    })


def grazie(request):
    return render(request, "questionario/grazie.html")


@staff_member_required
def dashboard(request):
    totale = Risposta.objects.count()

    def freq(field, choices_class):
        qs = Risposta.objects.values(field).annotate(n=Count(field)).order_by(field)
        mapping = {v: l for v, l in choices_class.choices}
        return [
            {"label": mapping.get(r[field], r[field]), "n": r["n"], "pct": round(r["n"] / totale * 100) if totale else 0}
            for r in qs
        ]

    context = {
        "totale": totale,
        "q1": freq("q1_giro_affari", Risposta.GiroAffari),
        "q2": freq("q2_misura_dannosa", Risposta.MisuraDannosa),
        "q3": freq("q3_impatto_parcheggi", Risposta.ImpattoParcheggi),
        "q4": freq("q4_impatto_via_mazzini", Risposta.ImpattoViaMazzini),
        "q5": freq("q5_frequenza_residenti", Risposta.FrequenzaResidenti),
        "q6": freq("q6_proposta", Risposta.Proposta),
        "q8": freq("q8_tipo_attivita", Risposta.TipoAttivita),
        "q9": freq("q9_posizione", Risposta.PosizioneAttivita),
        "q10": freq("q10_contatto_disponibile", Risposta.DisponibileContatto),
        "note": Risposta.objects.exclude(q7_note="").values_list("q7_note", flat=True),
    }
    return render(request, "questionario/dashboard.html", context)
