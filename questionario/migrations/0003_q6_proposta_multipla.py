import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questionario", "0002_risposta_email"),
    ]

    # Il cambio di tipo varchar -> varchar[] richiede USING, che Django non
    # emette da solo: le risposte esistenti diventano array a un elemento.
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE questionario_risposta "
                        "ALTER COLUMN q6_proposta TYPE varchar(25)[] "
                        "USING CASE WHEN q6_proposta = '' THEN ARRAY[]::varchar(25)[] "
                        "ELSE ARRAY[q6_proposta]::varchar(25)[] END"
                    ),
                    reverse_sql=(
                        "ALTER TABLE questionario_risposta "
                        "ALTER COLUMN q6_proposta TYPE varchar(25) "
                        "USING COALESCE(q6_proposta[1], '')"
                    ),
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name="risposta",
                    name="q6_proposta",
                    field=django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("parcheggi_gratuiti", "Ripristinare i parcheggi gratuiti (anche solo in alcune fasce orarie)"),
                                ("via_mazzini", "Riaprire via Mazzini al traffico (almeno parzialmente)"),
                                ("permessi_residenti", "Reintrodurre i permessi per i residenti"),
                                ("ora_gratuita", "Prima ora di sosta gratuita ovunque"),
                                ("altro", "Altro (specificare)"),
                            ],
                            max_length=25,
                        ),
                        default=list,
                        size=None,
                    ),
                ),
            ],
        ),
    ]
