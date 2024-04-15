import sys
import json
import os
import asyncio

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from qasync import QEventLoop, QApplication

from web import HTTP
from pages import Home, Feed, Login, Register, Settings, Profile

class Application:

    def __init__(
        self
    ):
        self.geo = (0, 0, 1280, 720)
    
        self.qapp = QApplication(sys.argv)
        self.loop = QEventLoop(self.qapp)
        self.running = True
        asyncio.set_event_loop(self.loop)

        self.close_event = asyncio.Event()
        self.qapp.aboutToQuit.connect(self.stop_event_loop)

        self.widget = QWidget()
        self.widget.setWindowTitle("Planck")
        self.widget.setMinimumSize(*self.geo[2:4])
        self.widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        if not os.path.exists("cache.json"):
            with open("cache.json",'w') as c:
                json.dump({"theme":0}, c)
        with open("cache.json",'r') as c:
            self.theme = json.load(c).get('theme',0) # 0: light, 1: dark
        self.pages = {
            "home": Home(self),
            "feed" : Feed(self),
            "login": Login(self),
            "register": Register(self),
            "settings": Settings(self),
            "profile": Profile(self),
        }


    @property
    def icon_path(self):
        if self.theme == 0:
            return "assets/images/planck.png"
        elif self.theme == 1:
            return "assets/images/planck-white.png"

    def stop_event_loop(self):
        self.close_event.set()
        for task in asyncio.all_tasks(self.loop):
            task.cancel()
        self.loop.stop()
        self.running = False

    def run(
        self
    ):
        self.http = HTTP(self)
        self.loop.create_task(self.http.start())
        self.loop.create_task(self.pages['home'].window())
        self.widget.setWindowIcon(QIcon("assets/images/planck.png"))
        # not using icon_path because it will be invisible on white background if theme is dark
        while self.running:
            try:
                self.loop.run_until_complete(self.close_event.wait())
            except (KeyboardInterrupt, asyncio.CancelledError):
                break

if __name__ == "__main__":
    app = Application()
    app.run()

