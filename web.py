from typing import TYPE_CHECKING
from collections import OrderedDict

import json
import requests
import base64

if TYPE_CHECKING:
    from Planck import Application


class HTTP:
    BASE = "https://c993213a-d982-4150-af94-01b86eca2c51-00-3gwqcj5yvvulu.janeway.replit.dev/api"

    def __init__(self, app):
        self.app: Application = app
        with open("cache.json", "r") as f:
            j = json.load(f)
            self.accounts = j.get("accounts", {})
            self.account = j.get("account", None)
        self.session = requests.Session()
        self.temp = {
            'pfp': Temp(30),
            'account': Temp(30)
        }

    def update_cache(self):
        with open("cache.json", "w") as f:
            json.dump({"accounts": self.accounts, "account": self.account, "theme": self.app.theme}, f)

    def request(self, endpoint, method, **kwargs):
        url = f"{self.BASE}/{endpoint}"
        if len(self.accounts) > 0:
            kwargs["headers"] = {
                "x-api-key": self.account['api_key']
            }
        response = self.session.request(method, url, **kwargs)
        return response

    def fetch_image(self, url, endpoint=True) -> bytes | None:
        if endpoint:
            if url.startswith("cdn"):
                e = url.split("/")
                if e[1] == "pfp":
                    if e[2] not in self.temp["pfp"]:
                        ret = self.request(url, "GET")
                        if ret.status_code == 200:
                            self.temp["pfp"][e[2]] = ret.content
                        else:
                            return None
                    return self.temp["pfp"][e[2]]
        else:
            ret = self.session.get(url)
            if ret.status_code == 200:
                return ret.content
            else:
                return None

    def fetch_account(self, username) -> dict | None:
        d = self.request(f"accounts/{username}", "GET")

    def login(self, username_or_email, password):
        data = {
            "username_or_email": username_or_email,
            "password": password
        }
        ret = self.request("accounts/login", "POST", json=data)
        if ret.status_code == 200:
            rj = ret.json()
            return rj
        else:
            return False

    def logout(self, api_key):
        self.accounts.pop(self.account)
        self.account = self.accounts.values()[0] if len(self.accounts) > 0 else None

    def register(self, username, name, password, email, birthdate):

        data = {
            "username": username,
            "name": name,
            "password": password,
            "email": email,
            "birthdate": birthdate.isoformat(),
        }
        ret = self.request("accounts/create", "POST", json=data)
        if ret.status_code == 200:
            rj = ret.json()
            return rj
        else:
            return False

    def update_account(self, username, name, password, email, birthdate, pfp):
        if pfp:
            with open(pfp, "rb") as f:
                pfp = [pfp.split("/")[-1], base64.b64encode(f.read()).decode()]
        data = {
            "username": username,
            "name": name,
            "password": password,
            "email": email,
            "birthdate": birthdate.isoformat(),
            "pfp": pfp
        }
        ret = self.request("accounts/update", "POST", json=data)
        if ret.status_code == 200:
            rj = ret.json()
            return rj
        else:
            return False

    def switch_account(
        self, api_key
    ):
        self.account = self.accounts[api_key]
        self.update_cache()
        self.app.pages["home"].open_page("home")

class Temp(OrderedDict):

    def __init__(self, max):
        super().__init__()
        self.max = max

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        if len(self) > self.max:
            self.popitem(last=False)
