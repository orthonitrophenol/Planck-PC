__all__ = ("Home",)


from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Home(Page):
    """The Home-page of Planck.
    """
    NAME = "home"

    async def window(
        self,
    ):

        w = self.widget
        l = self.layout
        w.setWindowTitle("Planck | Home")
        self.update_theme()

        tlayout = await self.title_layout()
        self.layout.addLayout(tlayout)

        nav_layout = await self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

