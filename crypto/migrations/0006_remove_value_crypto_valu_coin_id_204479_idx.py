# Generated by Django 3.2 on 2021-04-28 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0005_auto_20210428_1241"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="value", name="crypto_valu_coin_id_204479_idx",
        ),
    ]
