from typing import TYPE_CHECKING

import json
import requests

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

    def request(self, endpoint, method, **kwargs):
        url = f"{self.BASE}/{endpoint}"
        if len(self.accounts) > 0:
            kwargs["headers"] = {
                "Authorization": f"Bearer {self.accounts[0]['api_key']}"
            }
        response = self.session.request(method, url, **kwargs)
        return response

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

    def register(self, username, password, email, birthday, pfp_path = None):
        pfp = None
        if pfp_path:
            with open(pfp_path, "rb") as f:
                pfp = f.read()
        data = {
            "username": username,
            "password": password,
            "email": email,
            "birthday": birthday,
            "pfp": pfp
        }
        ret = self.request("accounts/register", "POST", json=data)
        if ret.status_code == 200:
            rj = ret.json()
            return rj
        else:
            return False

    def switch_account(
        self, api_key
    ):
        self.account = api_key
        self.app.pages["home"].window()
