# Generated by Django 3.2 on 2021-04-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0004_value_crypto_valu_coin_id_2abfdb_idx"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="value", name="crypto_valu_coin_id_2abfdb_idx",
        ),
        migrations.AddIndex(
            model_name="value",
            index=models.Index(
                fields=["coin", "date"], name="crypto_valu_coin_id_204479_idx"
            ),
        ),
    ]
