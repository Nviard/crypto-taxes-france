# Generated by Django 3.2.5 on 2021-10-24 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0010_cryptocomapptransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocomapptransaction',
            name='kind',
            field=models.CharField(choices=[('referral_card_cashback', 'Referral card cashback'), ('crypto_earn_interest_paid', 'Crypto earn interest paid'), ('exchange_to_crypto_transfer', 'Exchange to crypto transfer'), ('crypto_to_exchange_transfer', 'Crypto to exchange transfer'), ('reimbursement', 'Reimbursement'), ('crypto_earn_program_created', 'Crypto earn program created'), ('crypto_earn_program_withdrawn', 'Crypto earn program withdrawn'), ('supercharger_withdrawal', 'Supercharger withdrawal'), ('supercharger_deposit', 'Supercharger deposit'), ('card_top_up', 'Card top up'), ('crypto_purchase', 'Crypto purchase'), ('campaign_reward', 'Campaign reward'), ('crypto_dust_conversion', 'Crypto dust conversion')], max_length=32, null=True),
        ),
    ]
