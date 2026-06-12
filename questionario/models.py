from django.contrib.postgres.fields import ArrayField
from django.db import models


class Risposta(models.Model):
    # Q1
    class GiroAffari(models.TextChoices):
        CALATO_MOLTO = "calato_molto", "È calato molto"
        CALATO_UN_PO = "calato_un_po", "È calato un po'"
        UGUALE = "uguale", "È rimasto uguale"
        MIGLIORATO = "migliorato", "È migliorato"
        MOLTO_MIGLIORATO = "molto_migliorato", "È molto migliorato"

    # Q2
    class MisuraDannosa(models.TextChoices):
        ZONE_DISCO = "zone_disco", "Zone disco e parcheggi a pagamento in tutto il paese"
        VIA_MAZZINI = "via_mazzini", "Traffico limitato e rimozione parcheggi in via Mazzini"
        PERMESSI = "permessi", "Annullamento dei permessi di sosta per i residenti del centro"
        TUTTE = "tutte", "Tutte e tre allo stesso modo"
        NESSUNA = "nessuna", "Nessuna in particolare"

    # Q3
    class ImpattoParcheggi(models.TextChoices):
        SI_MOLTI = "si_molti", "Sì, molti evitano di venire in centro"
        SI_QUALCUNO = "si_qualcuno", "Sì, ma solo qualcuno"
        NO = "no", "No, non ho notato differenze"
        NON_SO = "non_so", "Non so / difficile dirlo"

    # Q4
    class ImpattoViaMazzini(models.TextChoices):
        SI_SERI = "si_seri", "Sì, problemi seri (carico/scarico difficile, clienti in meno)"
        QUALCHE = "qualche", "Qualche disagio, ma gestibile"
        NO = "no", "No, non mi ha riguardato"
        NON_APP = "non_app", "Non applicabile alla mia attività"

    # Q5
    class FrequenzaResidenti(models.TextChoices):
        MENO = "meno", "No, ne vedo meno"
        UGUALE = "uguale", "Più o meno uguale"
        NON_SO = "non_so", "Non saprei dirlo"

    # Q6
    class Proposta(models.TextChoices):
        PARCHEGGI_GRATUITI = "parcheggi_gratuiti", "Ripristinare i parcheggi gratuiti (anche solo in alcune fasce orarie)"
        VIA_MAZZINI = "via_mazzini", "Riaprire via Mazzini al traffico (almeno parzialmente)"
        PERMESSI_RESIDENTI = "permessi_residenti", "Reintrodurre i permessi per i residenti"
        ORA_GRATUITA = "ora_gratuita", "Prima ora di sosta gratuita ovunque"
        ALTRO = "altro", "Altro (specificare)"

    # Q8
    class TipoAttivita(models.TextChoices):
        DETTAGLIO = "dettaglio", "Negozio al dettaglio"
        BAR_RISTORANTE = "bar_ristorante", "Bar / ristorante / pasticceria"
        SERVIZI = "servizi", "Servizi (studio professionale, parrucchiere, ecc.)"
        ALTRO = "altro", "Altro"

    # Q9
    class PosizioneAttivita(models.TextChoices):
        VIA_MAZZINI = "via_mazzini", "Sì, in via Mazzini"
        VICINANZE = "vicinanze", "No, ma nelle immediate vicinanze"
        ALTRA_ZONA = "altra_zona", "No, in un'altra zona del centro"

    # Q10
    class DisponibileContatto(models.TextChoices):
        SI = "si", "Sì, volentieri"
        FORSE = "forse", "Forse, dipende"
        NO = "no", "No, preferisco restare anonimo"

    # Fields
    q1_giro_affari = models.CharField(max_length=20, choices=GiroAffari.choices)
    q2_misura_dannosa = models.CharField(max_length=20, choices=MisuraDannosa.choices)
    q3_impatto_parcheggi = models.CharField(max_length=20, choices=ImpattoParcheggi.choices)
    q4_impatto_via_mazzini = models.CharField(max_length=20, choices=ImpattoViaMazzini.choices)
    q5_frequenza_residenti = models.CharField(max_length=10, choices=FrequenzaResidenti.choices)
    # Risposta multipla: lista di valori di Proposta
    q6_proposta = ArrayField(models.CharField(max_length=25, choices=Proposta.choices), default=list)
    q7_note = models.TextField(blank=True)
    q8_tipo_attivita = models.CharField(max_length=20, choices=TipoAttivita.choices)
    q9_posizione = models.CharField(max_length=15, choices=PosizioneAttivita.choices)
    q10_contatto_disponibile = models.CharField(max_length=10, choices=DisponibileContatto.choices)
    q10_recapito = models.CharField(max_length=200, blank=True)

    email = models.EmailField(blank=True)
    compilato_il = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-compilato_il"]
        verbose_name = "Risposta"
        verbose_name_plural = "Risposte"

    def __str__(self):
        return f"Risposta #{self.pk} — {self.compilato_il:%d/%m/%Y %H:%M}"
