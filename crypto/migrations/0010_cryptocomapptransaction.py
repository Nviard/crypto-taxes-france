# Generated by Django 3.2.5 on 2021-10-24 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0009_cryptocomtrade'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptocomAppTransaction',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.log')),
                ('kind', models.CharField(choices=[('referral_card_cashback', 'Referral card cashback'), ('crypto_earn_interest_paid', 'Crypto earn interest paid')], max_length=32, null=True)),
            ],
            bases=('crypto.log',),
        ),
    ]
