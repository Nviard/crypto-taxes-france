import sys
import asyncio
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
import cryptocom.exchange as cro
import keyring
from datetime import datetime
from datetime import date
from datetime import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from crypto.models import Coin
from crypto.models import Wallet
from crypto.models import CryptocomTrade
from crypto.models import CryptocomDeposit
from crypto.models import CryptocomWithdrawal
from collections import defaultdict

from typing import List

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret

account = cro.Account(
    api_key="#TODO obligatoire",
    api_secret=keyring.get_password("#TODO obligatoire", "#TODO obligatoire"),
)

async def account_get_trades(
    self,
    pair: cro.Pair = None,
    page: int = 0,
    page_size: int = 200,
    start_ts: int = None,
    end_ts: int = None,
) -> List[cro.PrivateTrade]:
    """Return trades."""
    params = {"page_size": page_size, "page": page}

    if start_ts:
        params["start_ts"] = int(start_ts) * 1000
    if end_ts:
        params["end_ts"] = int(end_ts) * 1000

    if pair:
        params["instrument_name"] = pair.name

    data = await self.api.post("private/get-trades", {"params": params})

    return [
        cro.PrivateTrade(
            id=int(trade["trade_id"]),
            side=cro.OrderSide(trade["side"]),
            pair=self.pairs[trade["instrument_name"]],
            fees=trade["fee"],
            fees_coin=cro.Coin(trade["fee_currency"]),
            created_at=int(trade["create_time"] / 1000),
            filled_price=trade["traded_price"],
            filled_quantity=trade["traded_quantity"],
            order_id=trade["order_id"],
        )
        for trade in data.get("trade_list") or []
    ]


def run():

    try:
        wallet = Wallet.objects.get(pk="Crypto.com Exchange")
    except ObjectDoesNotExist:
        wallet = Wallet(name="Crypto.com Exchange", provider="cryptocom")
        wallet.save()

    account.get_trades = async_to_sync(account_get_trades)
    account.get_deposit_history = async_to_sync(account.get_deposit_history)
    account.get_withdrawal_history = async_to_sync(account.get_withdrawal_history)
    account.sync_pairs = async_to_sync(account.sync_pairs)

    account.sync_pairs()
    account.pairs = keydefaultdict(lambda k: cro.Pair(k, price_precision=10, quantity_precision=10), account.pairs)

    CryptocomWithdrawal.objects.all().delete()
    start_ts = CryptocomWithdrawal.objects.aggregate(Max("time_executed"))[
        "time_executed__max"
    ]
    if start_ts:
        start_ts = int(datetime.timestamp(start_ts)) + 1
    else:
        start_ts = 15000000000

    page = 0

    while True:
        withdrawals = account.get_withdrawal_history(
            None, start_ts=start_ts, page=page, page_size=200
        )
        for w in withdrawals:
            pass
        page += 1

        if not withdrawals:
            break

    CryptocomDeposit.objects.all().delete()
    start_ts = CryptocomDeposit.objects.aggregate(Max("time_executed"))[
        "time_executed__max"
    ]
    if start_ts:
        start_ts = int(datetime.timestamp(start_ts)) + 1
    else:
        start_ts = 15000000000

    page = 0

    while True:
        deposits = account.get_deposit_history(
            None, start_ts=start_ts, page=page, page_size=200
        )
        for d in deposits:

            if d.create_time != d.update_time:
                print("Error, create_time is not equal to update_time")
                return

            if d.address in ["INTERNAL_DEPOSIT"]:
                continue

            if d.amount == 124.34512:
                continue

            quantity = d.amount
            currency = d.coin.name
            try:
                currency = Coin.objects.get(pk=currency)
            except ObjectDoesNotExist:
                currency = Coin(currency, last_update=date(1900, 1, 1))
                currency.save()

            deposit = CryptocomDeposit(
                time_executed=d.create_time.replace(tzinfo=timezone.utc),
                typ="deposit",
                bought_quantity=quantity,
                bought_currency=currency,
                sold_quantity=None,
                sold_currency=None,
                fee_quantity=None,
                fee_currency=None,
                classification="gift_received",
                wallet=wallet,
            )

            deposit.save()

        page += 1

        if not deposits:
            break

    #CryptocomTrade.objects.all().delete()
    start_ts = CryptocomTrade.objects.aggregate(Max("time_executed"))[
        "time_executed__max"
    ]
    if start_ts:
        start_ts = int(datetime.timestamp(start_ts))
    else:
        start_ts = 1577833200

    last_update = datetime.timestamp(datetime.now())

    while True:
        trades = account.get_trades(account, end_ts=last_update)
        for t in trades:
            last_update = t.created_at

            if start_ts == t.created_at:
                break

            if t.is_buy:
                bought_quantity = t.filled_quantity
                bought_currency = t.pair.base_coin.name
                sold_quantity = t.filled_quantity * t.filled_price
                sold_currency = t.pair.quote_coin.name
                fee_quantity = t.fees
                fee_currency = t.fees_coin.name
            else:
                bought_quantity = t.filled_quantity * t.filled_price
                bought_currency = t.pair.quote_coin.name
                sold_quantity = t.filled_quantity
                sold_currency = t.pair.base_coin.name
                fee_quantity = t.fees
                fee_currency = t.fees_coin.name

            try:
                bought_currency = Coin.objects.get(pk=bought_currency)
            except ObjectDoesNotExist:
                bought_currency = Coin(bought_currency, last_update=date(1900, 1, 1))
                bought_currency.save()

            try:
                sold_currency = Coin.objects.get(pk=sold_currency)
            except ObjectDoesNotExist:
                sold_currency = Coin(sold_currency, last_update=date(1900, 1, 1))
                sold_currency.save()

            try:
                fee_currency = Coin.objects.get(pk=fee_currency)
            except ObjectDoesNotExist:
                fee_currency = Coin(fee_currency, last_update=date(1900, 1, 1))
                fee_currency.save()

            trade = CryptocomTrade(
                time_executed=datetime.fromtimestamp(t.created_at, timezone.utc),
                typ="order",
                bought_quantity=bought_quantity,
                bought_currency=bought_currency,
                sold_quantity=sold_quantity,
                sold_currency=sold_currency,
                fee_quantity=fee_quantity,
                fee_currency=fee_currency,
                classification="",
                wallet=wallet,
                crypto_id=t.id,
            )

            trade.save()

        if start_ts == t.created_at:
            break

        if not trades:
            last_update -= 24 * 60 * 60
            if last_update < start_ts:
                last_update = start_ts


if (
    sys.version_info[0] == 3
    and sys.version_info[1] >= 8
    and sys.platform.startswith("win")
):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
