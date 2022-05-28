import csv

from datetime import date
from datetime import datetime
from datetime import timezone
from django.core.exceptions import ObjectDoesNotExist
from crypto.models import Coin
from crypto.models import NexoTransaction
from crypto.models import Wallet

NexoTransaction.objects.all().delete()

tzlocal = datetime.now().astimezone().tzinfo

def run():
    trades = []
    incomes = []
    outcomes = []

    try:
        wallet_nexo = Wallet.objects.get(pk="Nexo")
    except ObjectDoesNotExist:
        wallet_nexo = Wallet(name="Nexo", provider="nexo")
        wallet_nexo.save()

    try:
        euro = Coin.objects.get(pk="EUR")
    except ObjectDoesNotExist:
        euro = Coin("EUR", last_update=date(1900, 1, 1))
        euro.save()

    with open("nexo.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader, None)
        for row in spamreader:
            if row[1] == "DepositToExchange":
                trades.append(
                    NexoTransaction(
                        time_executed=datetime.strptime(
                            row[9], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=tzlocal),
                        typ="deposit",
                        bought_quantity=float(row[3]),
                        bought_currency=euro,
                        sold_quantity=None,
                        sold_currency=None,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="add_funds",
                        wallet=wallet_nexo,
                    )
                )
            elif row[1] == "Exchange Cashback":
                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()
                trades.append(
                    NexoTransaction(
                        time_executed=datetime.strptime(
                            row[9], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=tzlocal),
                        typ="deposit",
                        bought_quantity=float(row[3]),
                        bought_currency=currency,
                        sold_quantity=None,
                        sold_currency=None,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="income",
                        wallet=wallet_nexo,
                    )
                )
            elif row[1] == "Exchange":
                sold_currency = row[2]
                if sold_currency == "EURX":
                    sold_currency = "EUR"
                try:
                    sold_currency = Coin.objects.get(pk=sold_currency)
                except ObjectDoesNotExist:
                    sold_currency = Coin(sold_currency, last_update=date(1900, 1, 1))
                    sold_currency.save()
                bought_currency = row[4]
                try:
                    bought_currency = Coin.objects.get(pk=bought_currency)
                except ObjectDoesNotExist:
                    bought_currency = Coin(bought_currency, last_update=date(1900, 1, 1))
                    bought_currency.save()
                trades.append(
                    NexoTransaction(
                        time_executed=datetime.strptime(
                            row[9], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=tzlocal),
                        typ="order",
                        bought_quantity=float(row[5]),
                        bought_currency=bought_currency,
                        sold_quantity=-float(row[3]),
                        sold_currency=sold_currency,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="",
                        wallet=wallet_nexo,
                    )
                )
            elif row[1] in ["LockingTermDeposit", "ExchangeDepositedOn"]:
                continue
            else:
                print(row)
                break
                
    for t in trades:
        t.save()
