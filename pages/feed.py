__all__ = ("Feed",)

from typing import List, Dict, Any

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Feed(Page):
    """The user's feed is shown here.
    """
    NAME = "feed"

    def __init__(
        self,
        app
    ):
        super().__init__(app)
        self.posts: List[Dict[str, Any]] = []

    def window(
        self,
    ):

        w = self.widget
        l = self.layout
        w.setWindowTitle("Planck | Feed")
        self.update_theme()
        tlayout = self.title_layout()
        self.layout.addLayout(tlayout)

        nav_layout = self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

