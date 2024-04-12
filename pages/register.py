__all__ = ("Register",)

from typing import List, Dict, Any

import json

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Register(Page):
    """The register page.
    """
    NAME = "register"

    def __init__(
        self,
        app
    ):
        super().__init__(app)

    def register(self):
        u = self.app.http.register(
            self.username_input.text(),
            self.password_input.text(),
            self.email_input.text(),
            self.birthday_input.date().toString("yyyy-MM-dd"),
            self.pfp_path,
        )
        if u:
            self.app.http.accounts[u['api_key']] = u
            self.app.http.account = u
            with open("cache.json", "w") as f:
                json.dump({"accounts": self.app.http.accounts, "account": u}, f)
            self.open_page("home")

    def upload_pfp(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.pfp_path, _ = QFileDialog.getOpenFileName(self.widget, 'Upload Profile Picture', '', 'Images (*.png *.xpm *.jpg *.jpeg)', options=options)

    def register_layout(self):
        register_layout = QVBoxLayout()
        register_layout.setAlignment(Qt.AlignCenter)

        username_label = QLabel('Username or Email:')
        register_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(300)
        register_layout.addWidget(self.username_input)

        password_label = QLabel('Password:')
        register_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setFixedWidth(300)
        self.password_input.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.password_input)

        email_label = QLabel('Email:')
        register_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setFixedWidth(300)
        register_layout.addWidget(self.email_input)

        birthday_label = QLabel('Birthday:')
        register_layout.addWidget(birthday_label)
        self.birthday_input = QDateEdit()
        self.birthday_input.setFixedWidth(300)
        self.birthday_input.setCalendarPopup(True)
        register_layout.addWidget(self.birthday_input)

        pfp_label = QLabel('Profile Picture:')
        register_layout.addWidget(pfp_label)
        self.pfp_button = QPushButton('Upload')
        self.pfp_button.clicked.connect(self.upload_pfp)
        self.pfp_button.setFixedWidth(300)
        register_layout.addWidget(self.pfp_button, alignment=Qt.AlignCenter)

        register_button = QPushButton('Register')
        register_button.setFixedWidth(200)
        register_button.clicked.connect(self.register)
        register_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        return register_layout


    def window(self):
        w = self.widget
        l = self.layout  # Create a QVBoxLayout instance
        w.setWindowTitle("Planck | register")

        tlayout = self.title_layout()
        l.addLayout(tlayout)

        register_layout = self.register_layout()
        l.addLayout(register_layout)

        nav_layout = self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

