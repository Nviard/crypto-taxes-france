import csv

from datetime import date
from datetime import datetime
from datetime import timezone
from django.core.exceptions import ObjectDoesNotExist
from crypto.models import Coin
from crypto.models import UpholdTransaction
from crypto.models import Wallet

UpholdTransaction.objects.all().delete()


def run():
    trades = []
    incomes = []
    outcomes = []

    try:
        wallet_uphold = Wallet.objects.get(pk="Uphold")
    except ObjectDoesNotExist:
        wallet_uphold = Wallet(name="Uphold", provider="uphold")
        wallet_uphold.save()

    try:
        wallet_cred = Wallet.objects.get(pk="Cred")
    except ObjectDoesNotExist:
        wallet_cred = Wallet(name="Cred", provider="other_exchange")
        wallet_cred.save()

    try:
        wallet_cryptoexchange = Wallet.objects.get(pk="Crypto.com Exchange")
    except ObjectDoesNotExist:
        wallet_cryptoexchange = Wallet(name="Crypto.com Exchange", provider="cryptocom")
        wallet_cryptoexchange.save()

    try:
        euro = Coin.objects.get(pk="EUR")
    except ObjectDoesNotExist:
        euro = Coin("EUR", last_update=date(1900, 1, 1))
        euro.save()

    with open("uphold.csv") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader, None)
        for row in spamreader:
            if row[10] == "completed":
                if row[11] == "in":
                    if row[1] == "uphold" and row[7] == "uphold":
                        currency = row[3]
                        try:
                            currency = Coin.objects.get(pk=currency)
                        except ObjectDoesNotExist:
                            currency = Coin(currency, last_update=date(1900, 1, 1))
                            currency.save()

                        quantity = float(row[2])

                        incomes.append(
                            (
                                datetime.strptime(
                                    row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                ).replace(tzinfo=timezone.utc),
                                quantity,
                                currency,
                            )
                        )
                    else:
                        print(row)
                        break
                elif row[11] == "transfer":
                    if row[1] == "uphold" and row[7] == "uphold":
                        bought_currency = row[3]
                        try:
                            bought_currency = Coin.objects.get(pk=bought_currency)
                        except ObjectDoesNotExist:
                            bought_currency = Coin(
                                bought_currency, last_update=date(1900, 1, 1)
                            )
                            bought_currency.save()

                        bought_quantity = float(row[2])

                        sold_currency = row[9]
                        try:
                            sold_currency = Coin.objects.get(pk=sold_currency)
                        except ObjectDoesNotExist:
                            sold_currency = Coin(
                                sold_currency, last_update=date(1900, 1, 1)
                            )
                            sold_currency.save()

                        sold_quantity = float(row[8])

                        if (
                            bought_currency == sold_currency
                            and bought_quantity == sold_quantity
                        ):
                            continue

                        trades.append(
                            UpholdTransaction(
                                time_executed=datetime.strptime(
                                    row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                ).replace(tzinfo=timezone.utc),
                                typ="order",
                                bought_quantity=bought_quantity,
                                bought_currency=bought_currency,
                                sold_quantity=sold_quantity,
                                sold_currency=sold_currency,
                                fee_quantity=None,
                                fee_currency=None,
                                classification="",
                                wallet=wallet_uphold,
                            )
                        )
                    else:
                        print(row)
                        break
                elif row[11] == "out":
                    if row[1] == "uphold" and row[7] == "uphold":
                        currency = row[3]
                        try:
                            currency = Coin.objects.get(pk=currency)
                        except ObjectDoesNotExist:
                            currency = Coin(currency, last_update=date(1900, 1, 1))
                            currency.save()

                        quantity = float(row[2])

                        inc = next(
                            (
                                i
                                for i in range(len(incomes))
                                if incomes[i][0]
                                == datetime.strptime(
                                    row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                ).replace(tzinfo=timezone.utc)
                            ),
                            None,
                        )
                        if inc is not None:
                            inc = incomes.pop(inc)
                            trades.append(
                                UpholdTransaction(
                                    time_executed=inc[0],
                                    typ="order",
                                    bought_quantity=inc[1],
                                    bought_currency=inc[2],
                                    sold_quantity=quantity,
                                    sold_currency=currency,
                                    fee_quantity=None,
                                    fee_currency=None,
                                    classification="",
                                    wallet=wallet_uphold,
                                )
                            )
                        else:
                            trades.append(
                                UpholdTransaction(
                                    time_executed=datetime.strptime(
                                        row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                    ).replace(tzinfo=timezone.utc),
                                    typ="withdraw",
                                    bought_quantity=None,
                                    bought_currency=None,
                                    sold_quantity=quantity,
                                    sold_currency=currency,
                                    fee_quantity=None,
                                    fee_currency=None,
                                    classification="internal",
                                    wallet=wallet_uphold,
                                )
                            )

                            trades.append(
                                UpholdTransaction(
                                    time_executed=datetime.strptime(
                                        row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                    ).replace(tzinfo=timezone.utc),
                                    typ="deposit",
                                    bought_quantity=quantity,
                                    bought_currency=currency,
                                    sold_quantity=None,
                                    sold_currency=None,
                                    fee_quantity=None,
                                    fee_currency=None,
                                    classification="internal",
                                    wallet=wallet_cred,
                                )
                            )

                            inc = next(
                                (
                                    i
                                    for i in range(len(incomes))
                                    if incomes[i][1] == quantity
                                    and incomes[i][2] == currency
                                ),
                                None,
                            )

                            if inc is not None:
                                inc = incomes.pop(inc)

                                trades.append(
                                    UpholdTransaction(
                                        time_executed=inc[0],
                                        typ="withdraw",
                                        bought_quantity=None,
                                        bought_currency=None,
                                        sold_quantity=quantity,
                                        sold_currency=currency,
                                        fee_quantity=None,
                                        fee_currency=None,
                                        classification="internal",
                                        wallet=wallet_cred,
                                    )
                                )

                                trades.append(
                                    UpholdTransaction(
                                        time_executed=inc[0],
                                        typ="deposit",
                                        bought_quantity=quantity,
                                        bought_currency=currency,
                                        sold_quantity=None,
                                        sold_currency=None,
                                        fee_quantity=None,
                                        fee_currency=None,
                                        classification="internal",
                                        wallet=wallet_uphold,
                                    )
                                )
                    elif row[1] == "" and row[7] == "uphold":

                        bought_currency = row[3]
                        try:
                            bought_currency = Coin.objects.get(pk=bought_currency)
                        except ObjectDoesNotExist:
                            bought_currency = Coin(
                                bought_currency, last_update=date(1900, 1, 1)
                            )
                            bought_currency.save()

                        bought_quantity = float(row[2])

                        sold_currency = row[9]
                        try:
                            sold_currency = Coin.objects.get(pk=sold_currency)
                        except ObjectDoesNotExist:
                            sold_currency = Coin(
                                sold_currency, last_update=date(1900, 1, 1)
                            )
                            sold_currency.save()

                        sold_quantity = float(row[8])

                        if row[4] and row[5]:
                            fee_currency = row[5]
                            try:
                                fee_currency = Coin.objects.get(pk=fee_currency)
                            except ObjectDoesNotExist:
                                fee_currency = Coin(
                                    sold_currency, last_update=date(1900, 1, 1)
                                )
                                fee_currency.save()

                            fee_quantity = float(row[4])
                        else:
                            fee_currency = None
                            fee_quantity = None

                        trades.append(
                            UpholdTransaction(
                                time_executed=datetime.strptime(
                                    row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                ).replace(tzinfo=timezone.utc),
                                typ="order",
                                bought_quantity=bought_quantity + (fee_quantity or 0),
                                bought_currency=bought_currency,
                                sold_quantity=sold_quantity,
                                sold_currency=sold_currency,
                                fee_quantity=fee_quantity,
                                fee_currency=fee_currency,
                                classification="",
                                wallet=wallet_uphold,
                            )
                        )

                        trades.append(
                            UpholdTransaction(
                                time_executed=datetime.strptime(
                                    row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                                ).replace(tzinfo=timezone.utc),
                                typ="withdraw",
                                bought_quantity=None,
                                bought_currency=None,
                                sold_quantity=bought_quantity,
                                sold_currency=bought_currency,
                                fee_quantity=None,
                                fee_currency=None,
                                classification="remove_funds",
                                wallet=wallet_uphold,
                            )
                        )

                    #TODO optionnel
                    # elif row[1] == "ethereum" and row[7] == "uphold":

                    #     bought_currency = row[3]
                    #     try:
                    #         bought_currency = Coin.objects.get(pk=bought_currency)
                    #     except ObjectDoesNotExist:
                    #         bought_currency = Coin(
                    #             bought_currency, last_update=date(1900, 1, 1)
                    #         )
                    #         bought_currency.save()

                    #     bought_quantity = float(row[2])

                    #     sold_currency = row[9]
                    #     try:
                    #         sold_currency = Coin.objects.get(pk=sold_currency)
                    #     except ObjectDoesNotExist:
                    #         sold_currency = Coin(
                    #             sold_currency, last_update=date(1900, 1, 1)
                    #         )
                    #         sold_currency.save()

                    #     sold_quantity = float(row[8])

                    #     fee_currency = row[5]
                    #     try:
                    #         fee_currency = Coin.objects.get(pk=fee_currency)
                    #     except ObjectDoesNotExist:
                    #         fee_currency = Coin(
                    #             sold_currency, last_update=date(1900, 1, 1)
                    #         )
                    #         fee_currency.save()

                    #     fee_quantity = float(row[4])

                    #     if (fee_quantity + bought_quantity) != sold_quantity:
                    #         print(
                    #             f"Error in quantities: {fee_quantity} + {bought_quantity} !=  {sold_quantity}"
                    #         )

                    #     trades.append(
                    #         UpholdTransaction(
                    #             time_executed=datetime.strptime(
                    #                 row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                    #             ).replace(tzinfo=timezone.utc),
                    #             typ="withdraw",
                    #             bought_quantity=None,
                    #             bought_currency=None,
                    #             sold_quantity=bought_quantity,
                    #             sold_currency=bought_currency,
                    #             fee_quantity=fee_quantity,
                    #             fee_currency=fee_currency,
                    #             classification="internal",
                    #             wallet=wallet_uphold,
                    #         )
                    #     )

                    #     trades.append(
                    #         UpholdTransaction(
                    #             time_executed=datetime.strptime(
                    #                 row[0], "%a %b %d %Y %H:%M:%S GMT+0000"
                    #             ).replace(tzinfo=timezone.utc),
                    #             typ="deposit",
                    #             bought_quantity=bought_quantity,
                    #             bought_currency=bought_currency,
                    #             sold_quantity=None,
                    #             sold_currency=None,
                    #             fee_quantity=None,
                    #             fee_currency=None,
                    #             classification="internal",
                    #             wallet=wallet_cryptoexchange,
                    #         )
                    #     )

                    else:
                        print(row)
                        break
                else:
                    print(row)
                    break
            else:
                print(f"Transaction not completed: {row[10]}")

    for inc in incomes:
        trades.append(
            UpholdTransaction(
                time_executed=inc[0],
                typ="deposit",
                bought_quantity=inc[1],
                bought_currency=inc[2],
                sold_quantity=None,
                sold_currency=None,
                fee_quantity=None,
                fee_currency=None,
                classification="income",
                wallet=wallet_uphold,
            )
        )
    for t in trades:
        t.save()
