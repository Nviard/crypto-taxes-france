# Generated by Django 3.2 on 2021-04-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crypto", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coin", name="last_update", field=models.DateTimeField(),
        ),
    ]