import csv

from datetime import date
from datetime import datetime
from datetime import timezone
from django.core.exceptions import ObjectDoesNotExist
from crypto.models import Coin
from crypto.models import CryptocomAppTransaction
from crypto.models import Wallet

CryptocomAppTransaction.objects.all().delete()


def run():
    trades = []
    to_remove = []
    crypto_dust_credited = {}
    crypto_dust_debited = {}

    try:
        wallet_cryptoapp = Wallet.objects.get(pk="Crypto.com App")
    except ObjectDoesNotExist:
        wallet_cryptoapp = Wallet(name="Crypto.com App", provider="cryptocom")
        wallet_cryptoapp.save()

    try:
        wallet_cryptoexchange = Wallet.objects.get(pk="Crypto.com Exchange")
    except ObjectDoesNotExist:
        wallet_cryptoexchange = Wallet(name="Crypto.com Exchange", provider="cryptocom")
        wallet_cryptoexchange.save()

    try:
        wallet_cryptoearn = Wallet.objects.get(pk="Crypto Earn")
    except ObjectDoesNotExist:
        wallet_cryptoearn = Wallet(name="Crypto Earn", provider="cryptocom")
        wallet_cryptoearn.save()

    try:
        wallet_cryptosupercharger = Wallet.objects.get(pk="Supercharger")
    except ObjectDoesNotExist:
        wallet_cryptosupercharger = Wallet(name="Supercharger", provider="cryptocom")
        wallet_cryptosupercharger.save()

    try:
        euro = Coin.objects.get(pk="EUR")
    except ObjectDoesNotExist:
        euro = Coin("EUR", last_update=date(1900, 1, 1))
        euro.save()

    with open("cryptocom.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader, None)
        for row in spamreader:
            if row[9] in (
                "referral_card_cashback",
                "crypto_earn_interest_paid",
                "reimbursement",
                "supercharger_reward_to_app_credited",
                "rewards_platform_deposit_credited",
            ):
                bought_currency = row[2]
                try:
                    bought_currency = Coin.objects.get(pk=bought_currency)
                except ObjectDoesNotExist:
                    bought_currency = Coin(
                        bought_currency, last_update=date(1900, 1, 1)
                    )
                    bought_currency.save()

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="deposit",
                        bought_quantity=float(row[3]),
                        bought_currency=bought_currency,
                        sold_quantity=None,
                        sold_currency=None,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="income",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )
            elif row[9] == "card_cashback_reverted":
                bought_currency = row[2]
                try:
                    bought_currency = Coin.objects.get(pk=bought_currency)
                except ObjectDoesNotExist:
                    bought_currency = Coin(
                        bought_currency, last_update=date(1900, 1, 1)
                    )
                    bought_currency.save()
                to_remove.append((abs(float(row[3])), bought_currency))
            elif row[9] in (
                "exchange_to_crypto_transfer",
                "crypto_to_exchange_transfer",
                "crypto_earn_program_created",
                "crypto_earn_program_withdrawn",
                "supercharger_withdrawal",
                "supercharger_deposit",
            ):
                if row[9] == "exchange_to_crypto_transfer":
                    source = wallet_cryptoexchange
                    destination = wallet_cryptoapp
                elif row[9] == "crypto_to_exchange_transfer":
                    source = wallet_cryptoapp
                    destination = wallet_cryptoexchange
                elif row[9] == "crypto_earn_program_created":
                    source = wallet_cryptoapp
                    destination = wallet_cryptoearn
                elif row[9] == "crypto_earn_program_withdrawn":
                    source = wallet_cryptoearn
                    destination = wallet_cryptoapp
                elif row[9] == "supercharger_withdrawal":
                    source = wallet_cryptosupercharger
                    destination = wallet_cryptoapp
                elif row[9] == "supercharger_deposit":
                    source = wallet_cryptoapp
                    destination = wallet_cryptosupercharger

                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()
                quantity = abs(float(row[3]))

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="withdraw",
                        bought_quantity=None,
                        bought_currency=None,
                        sold_quantity=quantity,
                        sold_currency=currency,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="internal",
                        wallet=source,
                        kind=row[9],
                    )
                )

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="deposit",
                        bought_quantity=quantity,
                        bought_currency=currency,
                        sold_quantity=None,
                        sold_currency=None,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="internal",
                        wallet=destination,
                        kind=row[9],
                    )
                )
            elif row[9] == "card_top_up":
                quantity_crypto = abs(float(row[3]))
                quantity_euro = abs(float(row[7]))

                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="order",
                        bought_quantity=quantity_euro,
                        bought_currency=euro,
                        sold_quantity=quantity_crypto,
                        sold_currency=currency,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="withdraw",
                        bought_quantity=None,
                        bought_currency=None,
                        sold_quantity=quantity_euro,
                        sold_currency=euro,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="remove_funds",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )
            elif row[9] == "crypto_purchase":
                quantity_crypto = abs(float(row[3]))
                quantity_euro = abs(float(row[7]))

                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="deposit",
                        bought_quantity=quantity_euro,
                        bought_currency=euro,
                        sold_quantity=None,
                        sold_currency=None,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="add_funds",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="order",
                        bought_quantity=quantity_crypto,
                        bought_currency=currency,
                        sold_quantity=quantity_euro,
                        sold_currency=euro,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )
            elif row[9] == "dust_conversion_credited":
                quantity = abs(float(row[3]))
                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()

                crypto_dust_credited[
                    datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=timezone.utc
                    )
                ] = (quantity, currency)
            elif row[9] == "dust_conversion_debited":
                quantity = abs(float(row[3]))
                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()
                crypto_dust_debited[
                    datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=timezone.utc
                    )
                ] = (quantity, currency)
            elif row[9] == "campaign_reward":
                quantity = abs(float(row[3]))
                currency = row[2]
                try:
                    currency = Coin.objects.get(pk=currency)
                except ObjectDoesNotExist:
                    currency = Coin(currency, last_update=date(1900, 1, 1))
                    currency.save()

                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="deposit",
                        bought_quantity=quantity,
                        bought_currency=currency,
                        sold_quantity=None,
                        sold_currency=None,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="gift_received",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )
            elif row[9] == "crypto_exchange":
                sold_quantity = abs(float(row[3]))
                sold_currency = row[2]
                try:
                    sold_currency = Coin.objects.get(pk=sold_currency)
                except ObjectDoesNotExist:
                    sold_currency = Coin(sold_currency, last_update=date(1900, 1, 1))
                    sold_currency.save()
                bought_quantity = abs(float(row[5]))
                bought_currency = row[4]
                try:
                    bought_currency = Coin.objects.get(pk=bought_currency)
                except ObjectDoesNotExist:
                    bought_currency = Coin(sold_currency, last_update=date(1900, 1, 1))
                    bought_currency.save()
                trades.append(
                    CryptocomAppTransaction(
                        time_executed=datetime.strptime(
                            row[0], "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=timezone.utc),
                        typ="order",
                        bought_quantity=bought_quantity,
                        bought_currency=bought_currency,
                        sold_quantity=sold_quantity,
                        sold_currency=sold_currency,
                        fee_quantity=None,
                        fee_currency=None,
                        classification="",
                        wallet=wallet_cryptoapp,
                        kind=row[9],
                    )
                )
            elif row[9] in ["lockup_lock", "lockup_unlock"]:
                pass
            else:
                print(row)
                print(f"Unknown: {row[9]}")
                break
    for r in to_remove:
        # print([i for i in range(len(trades)) if trades[i].kind == "referral_card_cashback" and trades[i].bought_quantity == r[0] and trades[i].bought_currency == r[1]])
        trades.pop(
            next(
                (
                    i
                    for i in range(len(trades))
                    if trades[i].kind == "referral_card_cashback"
                    and trades[i].bought_quantity == r[0]
                    and trades[i].bought_currency == r[1]
                ),
                None,
            )
        )
    if len(crypto_dust_credited) != len(crypto_dust_credited):
        raise (Exception("Crypto dust error"))
    for k in crypto_dust_credited:
        trades.append(
            CryptocomAppTransaction(
                time_executed=k,
                typ="order",
                bought_quantity=crypto_dust_credited[k][0],
                bought_currency=crypto_dust_credited[k][1],
                sold_quantity=crypto_dust_debited[k][0],
                sold_currency=crypto_dust_debited[k][1],
                fee_quantity=None,
                fee_currency=None,
                classification="",
                wallet=wallet_cryptoapp,
                kind="crypto_dust_conversion",
            )
        )
    for t in trades:
        t.save()
