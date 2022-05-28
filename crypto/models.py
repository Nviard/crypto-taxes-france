import csv
import urllib

from pycoingecko import CoinGeckoAPI
from datetime import datetime

from django.db import models
from django.utils.functional import cached_property


class Coin(models.Model):
    name = models.CharField(max_length=8, primary_key=True)
    coingecko_id = models.CharField(max_length=32)
    last_update = models.DateField()
    fiat = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def update_values(self):
        Value.objects.filter(coin=self).delete()
        if self.name == "USD":
            data = urllib.request.urlopen(
                "http://webstat.banque-france.fr/fr/downloadFile.do?id=5385698&exportType=csv"
            )
            cr = csv.reader(
                data.read().decode("utf-8-sig").splitlines()[6:], delimiter=";"
            )
            for row in cr:
                if row[38] != "-":
                    value = Value(
                        coin=self,
                        date=datetime(
                            int(row[0][6:10]), int(row[0][3:5]), int(row[0][:2])
                        ).date(),
                        value=1.0 / float(row[38].replace(",", ".")),
                    )
                    value.save()
        else:
            cg = CoinGeckoAPI()

            for date, price in cg.get_coin_market_chart_by_id(
                self.coingecko_id, "eur", "max"
            )["prices"]:
                value = Value(
                    coin=self,
                    date=datetime.utcfromtimestamp(date / 1000).date(),
                    value=price,
                )
                value.save()

        self.last_update = datetime.utcnow().date()
        self.save()

    def value(self, date):
        if self.name == "EUR":
            return 1.0
        if self.last_update < date:
            self.update_values()
        return (
            Value.objects.filter(coin=self, date__lte=date)
            .order_by("-date")
            .values("value")[0]["value"]
        )


class Value(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()

    class Meta:
        indexes = [models.Index(fields=["coin", "-date"])]


class Wallet(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    provider = models.CharField(max_length=16)


class Log(models.Model):
    time_executed = models.DateTimeField()
    TYPES = [
        ("deposit", "Deposit"),
        ("order", "Order"),
        ("withdraw", "Withdraw"),
    ]
    typ = models.CharField(max_length=16, choices=TYPES)
    bought_quantity = models.FloatField(null=True)
    bought_currency = models.ForeignKey(
        Coin, null=True, on_delete=models.RESTRICT, related_name="bought"
    )
    sold_quantity = models.FloatField(null=True)
    sold_currency = models.ForeignKey(
        Coin, null=True, on_delete=models.RESTRICT, related_name="sold"
    )
    fee_quantity = models.FloatField(null=True)
    fee_currency = models.ForeignKey(
        Coin, null=True, on_delete=models.RESTRICT, related_name="fee"
    )
    CLASSIFICATIONS = [
        ("add_funds", "Add funds"),
        ("gift_received", "Gift received"),
        ("ignored", "Ignored"),
        ("income", "Income"),
        ("internal", "Internal"),
        ("mined", "Mined"),
        ("remove_funds", "Remove funds"),
        ("staked", "Staked"),
    ]
    classification = models.CharField(max_length=16, choices=CLASSIFICATIONS, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.RESTRICT)

    @cached_property
    def bought_quantity_eur(self):
        return (
            self.bought_quantity * self.bought_currency.value(self.time_executed.date())
            if self.bought_quantity
            else 0.0
        )

    @cached_property
    def sold_quantity_eur(self):
        return (
            self.sold_quantity * self.sold_currency.value(self.time_executed.date())
            if self.sold_quantity
            else 0.0
        )

    @cached_property
    def fee_quantity_eur(self):
        return (
            self.fee_quantity * self.fee_currency.value(self.time_executed.date())
            if self.fee_quantity
            else 0.0
        )

    class Meta:
        indexes = [models.Index(fields=["time_executed", "typ"])]

class CryptocomTrade(Log):
    crypto_id = models.IntegerField(unique=True)

class CryptocomAppTransaction(Log):
    KINDS = [
        ("referral_card_cashback", "Referral card cashback"),
        ("crypto_earn_interest_paid", "Crypto earn interest paid"),
        ("exchange_to_crypto_transfer", "Exchange to crypto transfer"),
        ("crypto_to_exchange_transfer", "Crypto to exchange transfer"),
        ("reimbursement", "Reimbursement"),
        ("crypto_earn_program_created", "Crypto earn program created"),
        ("crypto_earn_program_withdrawn", "Crypto earn program withdrawn"),
        ("supercharger_withdrawal", "Supercharger withdrawal"),
        ("supercharger_deposit", "Supercharger deposit"),
        ("card_top_up", "Card top up"),
        ("crypto_purchase", "Crypto purchase"),
        ("campaign_reward", "Campaign reward"),
        ("crypto_dust_conversion", "Crypto dust conversion"),
        ("supercharger_reward_to_app_credited", "Supercharger reward to app credited"),
        ("crypto_exchange", "Crypto exchange"),
        ("rewards_platform_deposit_credited", "Rewards platform deposit credited"),
    ]
    kind = models.CharField(max_length=64, choices=KINDS, null=True)

class UpholdTransaction(Log):
    pass

class NexoTransaction(Log):
    pass

class CryptocomDeposit(Log):
    pass

class CryptocomWithdrawal(Log):
    pass

class CryptocomStakeInterest(Log):
    pass

class CryptocomTradeFeeRebate(Log):
    pass

class CryptocomSupercharger(Log):
    pass
