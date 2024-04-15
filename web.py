from __future__ import annotations

from typing import TYPE_CHECKING, Dict
from collections import OrderedDict

import json
import asyncio
import aiohttp
import base64

if TYPE_CHECKING:
    from Planck import Application, QEventLoop


class HTTP:
    BASE = "https://c993213a-d982-4150-af94-01b86eca2c51-00-3gwqcj5yvvulu.janeway.replit.dev/api"
    session: aiohttp.ClientSession
    temp: Dict[str, Temp]

    def __init__(self, app):
        self.app: Application = app
        self.loop: QEventLoop = app.loop
        self.started = asyncio.Event()
        with open("cache.json", "r") as f:
            j = json.load(f)
            self.accounts = j.get("accounts", {})
            self.account = j.get("account", None)
        self.temp = {
            'pfp': Temp(30),
            'account': Temp(30)
        }

    def update_cache(self):
        with open("cache.json", "w") as f:
            json.dump({"accounts": self.accounts, "account": self.account, "theme": self.app.theme}, f)

    async def request(self, method, endpoint, **kwargs) -> aiohttp.ClientResponse:
        await self.started.wait()
        url = f"{self.BASE}/{endpoint}"
        if len(self.accounts) > 0:
            h = kwargs['headers'] if 'headers' in kwargs else {}
            h["x-api-key"] = h.get('api_key', self.account['api_key'])
            kwargs['headers'] = h
            
        async with self.session.request(method, url, **kwargs) as response:
            if response.status == 200:
                ct = response.content_type
                if ct == "application/json":
                    return await response.json()
                else:
                    return await response.content.read()

    async def fetch_image(self, url, endpoint=True) -> bytes | None:
        if endpoint:
            if url.startswith("cdn"):
                e = url.split("/")
                if e[1] == "pfp":
                    if e[2] not in self.temp["pfp"]:
                        ret = await self.request("GET", url)
                        if ret:
                            self.temp["pfp"][e[2]] = ret
                        else:
                            return None
                    return self.temp["pfp"][e[2]]
        else:
            ret = await self.session.get(url)
            if ret.status_code == 200:
                return await ret.content.read()


    async def fetch_account(self, username) -> dict | None:
        return await self.request("GET", f"accounts/{username}")

    async def search_accounts(self, query) -> dict | None:
        return await self.request("GET", f"accounts/search/{query}")

    async def login(self, username_or_email, password) -> dict | bool:
        data = {
            "username_or_email": username_or_email,
            "password": password
        }
        return await self.request("POST", "accounts/login", json=data)

    def logout(self):
        self.accounts.pop(self.account['api_key'])
        self.account = None
        self.update_cache()

    async def register(self, username, name, password, email, birthdate):

        data = {
            "username": username,
            "name": name,
            "password": password,
            "email": email,
            "birthdate": birthdate.isoformat(),
        }
        return await self.request("POST", "accounts/create", json=data)

    async def update_account(self, username, name, password, email, birthdate, pfp):
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
        return await self.request("POST", "accounts/update", json=data)

    async def switch_account(
        self, api_key: str
    ):
        self.account = a = await self.request("GET", f"accounts/me", headers={"x-api-key": api_key})
        self.accounts[a]['api_key'] = api_key
        self.update_cache()
        await self.app.pages["home"].open_page("home")


    async def start(self):
        self.session = aiohttp.ClientSession()
        self.started.set()
        u = await self.request("GET", "accounts/me")

        if u:
            self.account = u
            self.accounts[u['api_key']] = u
            self.update_cache()


class Temp(OrderedDict):

    def __init__(self, max):
        super().__init__()
        self.max = max

    def __setitem__(self, k, v):
        super().__setitem__(k, v)
        if len(self) > self.max:
            self.popitem(last=False)
