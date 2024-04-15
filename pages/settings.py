__all__ = ("Settings",)

from typing import List, Dict, Any
from datetime import date
import json

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Settings(Page):
    """The user's settings are shown here.
    """
    NAME = "settings"

    def __init__(
        self,
        app
    ):
        super().__init__(app)

    def save_settings(self):
        async def _internal():
            uname = self.username_input.text()
            name = self.name_input.text()
            pword = self.password_input.text()
            email = self.email_input.text()
            birthdate = self.birthdate_input.date().toPyDate()

            pfp = self.pfp_path
            theme = self.theme_input.currentIndex()
            if self.app.theme != theme:
                self.app.theme = theme
                await self.reload()
                with open("cache.json", "w") as f:
                    self.app.http.update_cache()
            if not (len(uname) ==  len(name) == len(pword) == len(email) == len(pfp) == 0) or birthdate.isoformat() != self.app.http.account['birthdate']:
                u = await self.app.http.update_account(
                    uname if len(uname) > 0 else None,
                    name if len(name) > 0 else None,
                    pword if len(pword) > 0 else None,
                    email if len(email) > 0 else None,
                    birthdate,
                    pfp if len(pfp) > 0 else None
                )
                if u:
                    self.app.http.accounts[u['api_key']] = u
                    self.app.http.account = u
                    self.app.http.update_cache()
                    await self.clear_layout(self.layout)
                    await self.app['home'].window()
        self.app.loop.create_task(_internal())

    def change_theme(self):
        async def _internal():
            self.app.theme = self.theme_input.currentIndex()
            self.update_theme()
            await self.reload()
            if hasattr(self, "sw"):
                self.sw.setStyleSheet(self.get_css("submit_button"))
                for wt in [QLineEdit, QComboBox, QTextEdit, QDateEdit, QPushButton]:
                    for w in self.sw.findChildren(wt):
                        w.setStyleSheet(self.get_css("input"))
                for wt in [QLabel]:
                    for w in self.sw.findChildren(wt):
                        w.setStyleSheet(self.get_css("anti_theme"))
        self.update_theme()
        self.loop.create_task(_internal())

    def upload_pfp(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.pfp_path, _ = QFileDialog.getOpenFileName(self.widget, 'Upload Profile Picture', '', 'Images (*.png *.xpm *.jpg *.jpeg)', options=options)
        if self.pfp_path:
            self.pfp_button.setIcon(QIcon(self.create_circular_pixmap(QPixmap.fromImage(QImage(self.pfp_path)))))

    async def settings_widget(self):
        settings_layout = QVBoxLayout()
        settings_layout.setAlignment(Qt.AlignCenter)

        pfp_label = QLabel('Profile Picture:')
        settings_layout.addWidget(pfp_label)

        pfp_path = self.app.http.account['pfp']
        self.pfp_path = ''
        if len(pfp_path) > 0:
            purl = 'cdn/pfp/' + pfp_path
            p = await self.app.http.fetch_image(purl)
            self.pfp_button, pm = self.image(p, content = True)
        else:
            self.pfp_button, pm = self.image(self.app.icon_path)
        pm = self.create_circular_pixmap(pm)
        self.pfp_button.setIcon(QIcon(pm))
        icon_size = 100
        self.pfp_button.setIconSize(QSize(icon_size, icon_size))
        self.pfp_button.setStyleSheet("border: none;")
        self.pfp_button.clicked.connect(self.upload_pfp)
        settings_layout.addWidget(self.pfp_button)

        username_label = QLabel('Username:')
        settings_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(300)
        self.username_input.setStyleSheet(self.get_css("input"))
        settings_layout.addWidget(self.username_input)

        name_label = QLabel('Name:')
        settings_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(300)
        self.name_input.setStyleSheet(self.get_css("input"))
        settings_layout.addWidget(self.name_input)

        password_label = QLabel('Password:')
        settings_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setFixedWidth(300)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.get_css("input"))
        settings_layout.addWidget(self.password_input)

        email_label = QLabel('Email:')
        settings_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setFixedWidth(300)
        self.email_input.setStyleSheet(self.get_css("input"))
        settings_layout.addWidget(self.email_input)

        birthdate_label = QLabel('Birthdate:')
        settings_layout.addWidget(birthdate_label)
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDate(QDate.fromString(self.app.http.account['birthdate'],'yyyy-MM-dd'))
        self.birthdate_input.setStyleSheet(self.get_css("input"))
        settings_layout.addWidget(self.birthdate_input)

        theme_label = QLabel('Theme:')
        settings_layout.addWidget(theme_label)
        self.theme_input = QComboBox()
        self.theme_input.addItem("Light")
        self.theme_input.addItem("Dark")
        self.theme_input.setCurrentIndex(self.app.theme)
        self.theme_input.currentIndexChanged.connect(self.change_theme)
        self.theme_input.setStyleSheet(self.get_css("input"))
        settings_layout.addWidget(self.theme_input)

        self.settings_button = QPushButton('Save')
        self.settings_button.clicked.connect(self.save_settings)
        self.settings_button.setFixedWidth(200)
        self.settings_button.setStyleSheet(self.get_css("anti_submit_button"))
        settings_layout.addWidget(self.settings_button,  alignment=Qt.AlignCenter)

        settings_widget = QWidget()
        settings_widget.setLayout(settings_layout)
        settings_widget.setFixedWidth(500)
        settings_widget.setStyleSheet(self.get_css('submit_button'))

        return settings_widget

    async def window(
        self,
    ):

        w = self.widget
        l = self.layout
        w.setWindowTitle("Planck | Settings")

        tlayout = await self.title_layout()
        self.layout.addLayout(tlayout)
        self.layout.addStretch(1)

        self.sw = sw = await self.settings_widget()
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

