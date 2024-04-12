__all__ = ("Upload",)

from typing import List, Dict, Any

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Upload(Page):
    """The user's feed is shown here.
    """
    NAME = "upload"

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
        w.setWindowTitle("Planck | Upload")
        tlayout = self.title_layout()
        self.layout.addLayout(tlayout)

        nav_layout = self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

