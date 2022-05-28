import csv

from datetime import datetime
from datetime import date
from datetime import timedelta
from datetime import timezone
from django.core.exceptions import ObjectDoesNotExist
from crypto.models import Coin
from crypto.models import CryptocomStakeInterest
from crypto.models import CryptocomTradeFeeRebate
from crypto.models import CryptocomSupercharger
from crypto.models import Wallet


def run():

    try:
        wallet = Wallet.objects.get(pk="Crypto.com Exchange")
    except ObjectDoesNotExist:
        wallet = Wallet(name="Crypto.com Exchange", provider="cryptocom")
        wallet.save()

    CryptocomStakeInterest.objects.all().delete()
    with open("STAKE_INTEREST.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader, None)
        for row in spamreader:
            currency = row[4]
            try:
                currency = Coin.objects.get(pk=currency)
            except ObjectDoesNotExist:
                currency = Coin(currency, last_update=date(1900, 1, 1))
                currency.save()
            t = CryptocomStakeInterest(
                time_executed=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").replace(
                    tzinfo=timezone.utc
                ),
                typ="deposit",
                bought_quantity=float(row[5]),
                bought_currency=currency,
                sold_quantity=None,
                sold_currency=None,
                fee_quantity=None,
                fee_currency=None,
                classification="staked",
                wallet=wallet,
            )
            t.save()

    CryptocomTradeFeeRebate.objects.all().delete()
    with open("TRADE_FEE_REBATE.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader, None)
        for row in spamreader:
            currency = row[4]
            try:
                currency = Coin.objects.get(pk=currency)
            except ObjectDoesNotExist:
                currency = Coin(currency, last_update=date(1900, 1, 1))
                currency.save()

            t = CryptocomTradeFeeRebate(
                time_executed=datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f").replace(
                    tzinfo=timezone.utc
                ),
                typ="deposit",
                bought_quantity=float(row[5]),
                bought_currency=currency,
                sold_quantity=None,
                sold_currency=None,
                fee_quantity=None,
                fee_currency=None,
                classification="gift_received",
                wallet=wallet,
            )
            t.save()

    # CryptocomSupercharger.objects.all().delete()
    for currency, amount, date in (
        #TODO optionnel
        # (
        #     "UNI",
        #     1,
        #     datetime(2020, 11, 1, 8, 0, 0).replace(tzinfo=timezone.utc),
        # ),
        ,
    ):
        try:
            currency = Coin.objects.get(pk=currency)
        except ObjectDoesNotExist:
            currency = Coin(currency, last_update=date(1900, 1, 1))
            currency.save()
        for _ in range(30):
            t = CryptocomTradeFeeRebate(
                time_executed=date,
                typ="deposit",
                bought_quantity=amount,
                bought_currency=currency,
                sold_quantity=None,
                sold_currency=None,
                fee_quantity=None,
                fee_currency=None,
                classification="mined",
                wallet=wallet,
            )
            t.save()
            date += timedelta(days=1)
