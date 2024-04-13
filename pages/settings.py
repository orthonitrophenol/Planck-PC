__all__ = ("Settings",)

from typing import List, Dict, Any
from datetime import date
import json

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Settings(Page):
    """The user's feed is shown here.
    """
    NAME = "settings"

    def __init__(
        self,
        app
    ):
        super().__init__(app)
        self.posts: List[Dict[str, Any]] = []

    def save_settings(self):
        uname = self.username_input.text()
        name = self.name_input.text()
        pword = self.password_input.text()
        email = self.email_input.text()
        birthdate = self.birthdate_input.date().toPyDate()

        pfp = self.pfp_path
        theme = self.theme_input.currentIndex()
        if self.app.theme != theme:
            self.app.theme = theme
            self.open_page("settings")
            with open("cache.json", "w") as f:
                self.app.http.update_cache()
        if not (len(uname) ==  len(name) == len(pword) == len(email) == len(pfp) == 0) or birthdate.isoformat() != self.app.http.account['birthdate']:
            u = self.app.http.update_account(
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
                self.open_page("home")

    def change_theme(self):
        self.app.theme = self.theme_input.currentIndex()
        self.update_theme()

    def upload_pfp(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.pfp_path, _ = QFileDialog.getOpenFileName(self.widget, 'Upload Profile Picture', '', 'Images (*.png *.xpm *.jpg *.jpeg)', options=options)
        self.pfp_button.setIcon(QIcon(QPixmap.fromImage(QImage(self.pfp_path))))

    def settings_layout(self):
        settings_layout = QVBoxLayout()
        settings_layout.setAlignment(Qt.AlignCenter)

        pfp_label = QLabel('Profile Picture:')
        settings_layout.addWidget(pfp_label)

        pfp_path = self.app.http.account['pfp']
        self.pfp_path = ''
        if len(pfp_path) > 0:
            purl = 'cdn/pfp/' + pfp_path
            p = self.app.http.fetch_image(purl)
            pixmap = QPixmap()
            pixmap.loadFromData(p)
            self.pfp_button = QPushButton()
            self.pfp_button.setIcon(QIcon(pixmap))
        else:
            self.pfp_button, _ = self.image(self.app.icon_path)
        icon_size = 100
        self.pfp_button.setIconSize(QSize(icon_size, icon_size))
        self.pfp_button.setStyleSheet("border: none;")
        self.pfp_button.clicked.connect(self.upload_pfp)
        settings_layout.addWidget(self.pfp_button)

        username_label = QLabel('Username:')
        settings_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(300)
        settings_layout.addWidget(self.username_input)

        name_label = QLabel('Name:')
        settings_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(300)
        settings_layout.addWidget(self.name_input)

        password_label = QLabel('Password:')
        settings_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setFixedWidth(300)
        self.password_input.setEchoMode(QLineEdit.Password)
        settings_layout.addWidget(self.password_input)

        email_label = QLabel('Email:')
        settings_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setFixedWidth(300)
        settings_layout.addWidget(self.email_input)

        birthdate_label = QLabel('Birthdate:')
        settings_layout.addWidget(birthdate_label)
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDate(QDate.fromString(self.app.http.account['birthdate'],'yyyy-MM-dd'))
        settings_layout.addWidget(self.birthdate_input)

        theme_label = QLabel('Theme:')
        settings_layout.addWidget(theme_label)
        self.theme_input = QComboBox()
        self.theme_input.addItem("Light")
        self.theme_input.addItem("Dark")
        self.theme_input.setCurrentIndex(self.app.theme)
        self.theme_input.currentIndexChanged.connect(self.change_theme)
        settings_layout.addWidget(self.theme_input)


        settings_button = QPushButton('Save')
        settings_button.clicked.connect(self.save_settings)
        settings_button.setFixedWidth(200)
        settings_layout.addWidget(settings_button,  alignment=Qt.AlignCenter)


        return settings_layout

    def window(
        self,
    ):

        w = self.widget
        l = self.layout
        w.setWindowTitle("Planck | Settings")
        self.update_theme()

        tlayout = self.title_layout()
        self.layout.addLayout(tlayout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.settings_layout())

        nav_layout = self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

