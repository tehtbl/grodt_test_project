from time import sleep

import requests
from bitcoinaddress import Wallet

from config import celery_app
from grodt_test_project.mynewapp.models import MyNewAppModel


@celery_app.task()
def check_btc_wallet():
    """A pointless Celery task to demonstrate usage."""

    BASE_URL_CHECK = "https://blockchain.info/address/%(btcaddr)s?format=json"

    wallet = Wallet()

    pubkey = wallet.address.pubaddr1
    prvkey = wallet.address.privkey.wif

    reading_state = True
    reading_count = 0
    blockhain_info = {}
    while reading_state and reading_count < 4:
        try:
            r = requests.get(BASE_URL_CHECK % {
                "btcaddr": pubkey
            }, timeout=10)
            blockhain_info = r.json()
            reading_state = False
        except:
            reading_count += 1
            sleep(60 * reading_count)

    MyNewAppModel.objects.get_or_create(
        name="{}".format(prvkey[:5]),
        prvkey=prvkey,
        pubkey=pubkey,
        balance=float(blockhain_info['final_balance'])
    )

    return "Balance: {}".format(float(blockhain_info['final_balance']))
