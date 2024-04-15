__all__ = ("Profile",)

from typing import List, Dict, Any
from datetime import datetime
import json

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qasync import asyncSlot

class Profile(Page):
    """The user's profile page.
    """
    NAME = "profile"

    def __init__(
        self,
        app
    ):
        super().__init__(app)


    async def profile_widget(self):
        w = QWidget()
        w.setMinimumSize(500, 500)
        w.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        l = QVBoxLayout()
        w.setLayout(l)

        pfp_id = self.app.http.account['pfp']
        if len(pfp_id):
            pfp = await self.app.http.fetch_image(f'cdn/pfp/{pfp_id}')
            self.pfp_button, pm = self.image(pfp, content=True)
            pm = self.create_circular_pixmap(pm)
            self.pfp_button.setIcon(QIcon(pm))
            self.pfp_button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            self.pfp_button.setStyleSheet(self.get_css("anti_submit_button"))
            l.addWidget(self.pfp_button)

        self.username_label = ul = QLabel(f"@{self.app.http.account['username']}")
        uf = QFont('Arial', 25)
        uf.setBold(True)
        ul.setFont(uf)

        is_ver = self.app.http.account['verified']
        vl  = QLabel("✔️" if is_ver else None)
        vl.setFont(QFont('Arial', 15))
        vl.setToolTip("✔️ Verified" if is_ver else None)
        
        u_layout = QHBoxLayout()
        u_layout.addWidget(ul, 1)
        u_layout.addWidget(vl, 3)
        l.addLayout(u_layout)

        self.name_label = nl = QLabel(self.app.http.account['name'])
        nf = QFont('Arial', 20)
        nl.setFont(nf)
        l.setAlignment(nl, Qt.AlignLeft)
        l.addWidget(self.name_label)

        self.email_label = eb = QLabel("Email: {}".format(self.app.http.account['email']))
        eb.setFont(QFont('Arial', 15))
        l.addWidget(self.email_label)
        l.setAlignment(eb, Qt.AlignLeft)

        bd = datetime.strptime(self.app.http.account['birthdate'], '%Y-%m-%d')
        bd = bd.strftime(f'{bd.day} %B %Y')
        self.birthdate_label = bdl = QLabel(f"Birthdate: {bd}")
        bdl.setFont(QFont('Arial', 15))
        l.setAlignment(bdl, Qt.AlignLeft)
        l.addWidget(self.birthdate_label)

        w.setStyleSheet(
            self.get_css("submit_button")
        )

        return w

    async def window(
        self,
    ):

        w = self.widget
        l = self.layout
        w.setWindowTitle("Planck | Profile @{}".format(self.app.http.account['username']))

        tlayout = await self.title_layout()
        self.layout.addLayout(tlayout)
        self.layout.addStretch(1)

        self.sw = sw = await self.profile_widget()
        hl = QHBoxLayout()
        hl.addStretch(1)
        hl.addWidget(sw)
        hl.addStretch(1)
        self.layout.addLayout(hl)

        nav_layout = await self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        self.update_theme()
        w.show()

