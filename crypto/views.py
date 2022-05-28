import random
from collections import defaultdict
from datetime import date
from datetime import timedelta
import datetime as dt

from django.http import HttpResponse
from django.views.generic.base import TemplateView

from crypto.models import Log


class CryptoView(TemplateView):

    template_name = "crypto_view.html"

    @staticmethod
    def values_to_values_eur(values, date):
        return {k: v * k.value(date) for k, v in values.items()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        months = []
        months_check = []
        values = defaultdict(lambda: 0.0)
        values_75 = defaultdict(lambda: 0.0)
        values_50 = defaultdict(lambda: 0.0)
        values_25 = defaultdict(lambda: 0.0)
        values_0 = defaultdict(lambda: 0.0)
        cost = defaultdict(lambda: 0.0)
        real_cost = defaultdict(lambda: 0.0)
        gain = 0.0
        real_gain = 0.0
        taxes = []
        taxes_220 = 0.0
        taxes_221 = 0.0
        taxes_fraction = 0.0

        count = 0

        last_date = None

        if "platform" in kwargs:
            logs = Log.objects.all().filter(wallet=kwargs["platform"]).order_by("time_executed", "typ")
        else:
            logs = Log.objects.all().order_by("time_executed", "typ")

        for l in logs:

            # count +=1
            # if count > 2000-3:
            #     break
            r = random.random()

            if last_date is None:
                last_date = l.time_executed.date()
            elif (last_date.month != l.time_executed.date().month) or (
                last_date.year != l.time_executed.date().year
            ):
                while (last_date.month != l.time_executed.date().month) or (
                    last_date.year != l.time_executed.date().year
                ):
                    last_date = last_date.replace(day=28) + timedelta(days=4)
                    date = last_date.replace(day=1) - timedelta(days=1)
                    total_value = sum(
                        CryptoView.values_to_values_eur(values, date).values()
                    )
                    total_gain = total_value - sum(cost.values())
                    total_real_gain = total_value - sum(real_cost.values())
                    months.append(
                        [
                            date,
                            gain,
                            real_gain,
                            total_gain,
                            total_real_gain,
                            total_value,
                            total_real_gain + real_gain - total_gain - gain,
                            taxes_220 - taxes_221,
                        ]
                    )

                    total_value_75 = sum(
                        CryptoView.values_to_values_eur(values_75, date).values()
                    )
                    total_value_50 = sum(
                        CryptoView.values_to_values_eur(values_50, date).values()
                    )
                    total_value_25 = sum(
                        CryptoView.values_to_values_eur(values_25, date).values()
                    )
                    total_value_0 = sum(
                        CryptoView.values_to_values_eur(values_0, date).values()
                    )

                    months_check.append(
                        [
                            date,
                            total_value_0,
                            total_value_25,
                            total_value_50,
                            total_value_75,
                            total_value,
                            total_value - total_value_0,
                        ]
                    )

                last_date = l.time_executed.date()

            credit = l.bought_quantity
            debit = l.sold_quantity
            fee = l.fee_quantity
            credit_eur = l.bought_quantity_eur
            debit_eur = l.sold_quantity_eur
            fee_eur = l.fee_quantity_eur
            debit_eur_cost = (
                debit * cost[l.sold_currency] / values[l.sold_currency]
                if l.sold_currency and values[l.sold_currency]
                else 0.0
            )
            debit_eur_real_cost = (
                debit * real_cost[l.sold_currency] / values[l.sold_currency]
                if l.sold_currency and values[l.sold_currency]
                else 0.0
            )
            fee_eur_cost = (
                fee * cost[l.fee_currency] / values[l.fee_currency]
                if l.fee_currency and values[l.fee_currency]
                else 0.0
            )
            fee_eur_real_cost = (
                fee * real_cost[l.fee_currency] / values[l.fee_currency]
                if l.fee_currency and values[l.fee_currency]
                else 0.0
            )
            if l.classification == "remove_funds":
                gain += debit_eur - debit_eur_cost
                real_gain += debit_eur - debit_eur_real_cost
            if ("platform" in kwargs and l.classification != "ignored") or l.classification not in ["ignored", "internal"]:
                if l.bought_currency:
                    values[l.bought_currency] += credit
                if l.sold_currency:
                    values[l.sold_currency] -= debit
                if l.fee_currency:
                    values[l.fee_currency] -= fee
                if (
                    l.classification
                    or r < 0.75
                    or l.bought_currency.fiat
                    or l.sold_currency.fiat
                ):
                    if l.bought_currency:
                        values_75[l.bought_currency] += credit
                    if l.sold_currency:
                        values_75[l.sold_currency] -= debit
                    if l.fee_currency:
                        values_75[l.fee_currency] -= fee
                if (
                    l.classification
                    or r < 0.5
                    or l.bought_currency.fiat
                    or l.sold_currency.fiat
                ):
                    if l.bought_currency:
                        values_50[l.bought_currency] += credit
                    if l.sold_currency:
                        values_50[l.sold_currency] -= debit
                    if l.fee_currency:
                        values_50[l.fee_currency] -= fee
                if (
                    l.classification
                    or r < 0.25
                    or l.bought_currency.fiat
                    or l.sold_currency.fiat
                ):
                    if l.bought_currency:
                        values_25[l.bought_currency] += credit
                    if l.sold_currency:
                        values_25[l.sold_currency] -= debit
                    if l.fee_currency:
                        values_25[l.fee_currency] -= fee
                if l.classification or l.bought_currency.fiat or l.sold_currency.fiat:
                    if l.bought_currency:
                        values_0[l.bought_currency] += credit
                    if l.sold_currency:
                        values_0[l.sold_currency] -= debit
                    if l.fee_currency:
                        values_0[l.fee_currency] -= fee
                if l.classification in ["income", "gift_received", "staked", "mined", "reconcile"]:
                    cost[l.bought_currency] += credit_eur
                elif not l.classification:
                    cost[l.bought_currency] += debit_eur_cost
                    real_cost[l.bought_currency] += debit_eur_real_cost
                    if l.bought_currency != l.fee_currency:
                        cost[l.bought_currency] += fee_eur_cost
                        real_cost[l.bought_currency] += fee_eur_real_cost
                        cost[l.fee_currency] -= fee_eur_cost
                        real_cost[l.fee_currency] -= fee_eur_real_cost
                    cost[l.sold_currency] -= debit_eur_cost
                    real_cost[l.sold_currency] -= debit_eur_real_cost
                elif l.classification == "remove_funds":
                    cost[l.sold_currency] -= debit_eur_cost
                    real_cost[l.sold_currency] -= debit_eur_real_cost
                elif l.classification == "add_funds":
                    cost[l.bought_currency] += credit_eur
                    real_cost[l.bought_currency] += credit_eur
                if not l.classification and l.sold_currency.name == "EUR":
                    taxes_220 += debit_eur
                if (
                    not l.classification
                    or l.classification
                    in ["income", "gift_received", "staked", "mined", "reconcile"]
                ) and l.bought_currency.fiat:
                    taxes_211 = l.time_executed.date()
                    taxes_212 = (
                        sum(
                            (
                                v
                                for k, v in CryptoView.values_to_values_eur(
                                    values, l.time_executed.date()
                                ).items()
                                if not k.fiat
                            )
                        )
                        + credit_eur
                    )
                    taxes_213 = credit_eur
                    taxes_214 = fee_eur
                    taxes_215 = taxes_213 - taxes_214
                    taxes_216 = 0.0
                    taxes_217 = taxes_213 + taxes_216
                    taxes_218 = taxes_213 - taxes_214 + taxes_216
                    taxes_221 += taxes_fraction
                    taxes_222 = 0.0
                    taxes_223 = taxes_220 - taxes_221 - taxes_222
                    taxes_fraction = taxes_223 * taxes_217 / taxes_212
                    taxes_gain = taxes_218 - taxes_fraction
                    taxes.append(
                        [
                            taxes_211,
                            taxes_212,
                            taxes_213,
                            taxes_214,
                            taxes_215,
                            taxes_216,
                            taxes_217,
                            taxes_218,
                            taxes_220,
                            taxes_221,
                            taxes_222,
                            taxes_223,
                            taxes_gain,
                            taxes_fraction,
                        ]
                    )

        context["taxes"] = taxes
        context["months"] = months
        context["months_check"] = months_check

        values_eur = CryptoView.values_to_values_eur(values, dt.date.today())

        context["worth"] = sum(values_eur.values())
        
        context["summary"] = [
            [k.name, values[k], values_eur[k], cost[k], real_cost[k]]
            for k in sorted(values, key=lambda x: -values_eur[x])
        ]

        return context
