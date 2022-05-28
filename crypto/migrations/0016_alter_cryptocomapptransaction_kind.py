# Generated by Django 3.2.5 on 2021-11-20 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0015_alter_cryptocomapptransaction_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocomapptransaction',
            name='kind',
            field=models.CharField(choices=[('referral_card_cashback', 'Referral card cashback'), ('crypto_earn_interest_paid', 'Crypto earn interest paid'), ('exchange_to_crypto_transfer', 'Exchange to crypto transfer'), ('crypto_to_exchange_transfer', 'Crypto to exchange transfer'), ('reimbursement', 'Reimbursement'), ('crypto_earn_program_created', 'Crypto earn program created'), ('crypto_earn_program_withdrawn', 'Crypto earn program withdrawn'), ('supercharger_withdrawal', 'Supercharger withdrawal'), ('supercharger_deposit', 'Supercharger deposit'), ('card_top_up', 'Card top up'), ('crypto_purchase', 'Crypto purchase'), ('campaign_reward', 'Campaign reward'), ('crypto_dust_conversion', 'Crypto dust conversion'), ('supercharger_reward_to_app_credited', 'Supercharger reward to app credited'), ('crypto_exchange', 'Crypto exchange')], max_length=64, null=True),
        ),
    ]
