import requests

class API():

    def __init__(self, coin: str, callback: str, priority: str):
        self.coin = coin.lower()
        self.callback = callback
        self.priority = priority

        if not self.coin in ("btc", "ltc", "eth", "bch", "trx", "xmr"):
            raise Exception(
                "invalid coin. supported: (btc, ltc, eth, bch, trx, xmr)"
            )

        if not self.priority in ("fast", "default", "economic"):
            raise Exception(
                "invalid priority. supported: (fast, default, economic)"
            )

        self.client = requests.Session()
        self.base_url = "https://api.cryptapi.io/%s" % (self.coin)

    def prices(self):
        response = self.client.get(self.base_url + "/info")
        if response.json()["status"] == "success":
            return response.json()
        else:
            raise Exception(
                "failed to get %s's information. (%s)" % (self.coin, response.text)
            )

    def create_address(self, address: str, pending: str = "1", confirmations: str = "1", email: str = None, user: str = None):
        params = {
            "callback": self.callback if user == None else self.callback + "?user=%s" % (user),
            "address": address,
            "pending": pending,
            "confirmations": confirmations,
            "email": email,
            "priority": self.priority
        }

        response = self.client.get(self.base_url + "/create", params=params)
        if response.json()["status"] == "success":
            return response.json()
        else:
            raise Exception(
                "failed to create new address. (%s)" % (response.text)
            )

    def payment_logs(self):
        params = {
            "callback": self.callback
        }

        response = self.client.get(self.base_url + "/logs", params=params)
        if response.json()["status"] == "success":
            return response.json()
        else:
            raise Exception(
                "failed to get logs. (%s)" % (response.text)
            )
