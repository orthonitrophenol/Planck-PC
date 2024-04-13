import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from web import HTTP
from pages import Home, Feed, Login, Register, Settings

class Applciation:

    def __init__(
        self
    ):
        self.geo = (0, 0, 1280, 720)
        self.qapp = QApplication(sys.argv)
        self.widget = QWidget()
        self.widget.setWindowTitle("Planck")
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        with open("cache.json",'r') as c:
            self.theme = json.load(c).get('theme',0) # 0: light, 1: dark
        self.pages = {
            "home": Home(self),
            "feed" : Feed(self),
            "login": Login(self),
            "register": Register(self),
            "settings": Settings(self),
        }


    @property
    def icon_path(self):
        if self.theme == 0:
            return "assets/images/planck.png"
        elif self.theme == 1:
            return "assets/images/planck-white.png"

    def update(
        self
    ):
        self.widget.setGeometry(*self.geo)
        

    def run(
        self 
    ):
        self.http = HTTP(self)
        self.update()
        self.pages['home'].window()
        sys.exit(self.qapp.exec_())

if __name__ == "__main__":
    app = Applciation()
    app.run()

