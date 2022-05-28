# Generated by Django 3.2.5 on 2021-11-01 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0012_upholdtransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptocomDeposit',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.log')),
            ],
            bases=('crypto.log',),
        ),
        migrations.CreateModel(
            name='CryptocomInterest',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.log')),
            ],
            bases=('crypto.log',),
        ),
        migrations.CreateModel(
            name='CryptocomWithdrawal',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.log')),
            ],
            bases=('crypto.log',),
        ),
    ]
