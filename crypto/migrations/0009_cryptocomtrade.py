# Generated by Django 3.2.5 on 2021-10-21 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0008_log_crypto_log_time_ex_5ea5a8_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptocomTrade',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.log')),
                ('crypto_id', models.IntegerField(unique=True)),
            ],
            bases=('crypto.log',),
        ),
    ]
