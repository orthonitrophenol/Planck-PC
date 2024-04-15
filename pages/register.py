__all__ = ("Register",)

from typing import List, Dict, Any

import json

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qasync import asyncSlot

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
        async def _internal():
            u = await self.app.http.register(
                self.username_input.text(),
                self.name_input.text(),
                self.password_input.text(),
                self.email_input.text(),
                self.birthdate_input.date().toPyDate(),
            )
            if u:
                self.app.http.accounts[u['api_key']] = u
                self.app.http.account = u
                with open("cache.json", "w") as f:
                    json.dump({"accounts": self.app.http.accounts, "account": u, "theme": self.app.theme}, f)
                await self.clear_layout(self.layout)
                await self.app.pages['home'].window()
        self.app.loop.create_task(_internal())

    def toggle_password_visibility(self, password_input, checkbox):
        if checkbox.isChecked():
            password_input.setEchoMode(QLineEdit.Normal)
        else:
            password_input.setEchoMode(QLineEdit.Password)

    def register_layout(self):
        register_layout = QVBoxLayout()
        register_layout.setAlignment(Qt.AlignCenter)

        name_label = QLabel('Name:')
        register_layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(300)
        register_layout.addWidget(self.name_input)

        username_label = QLabel('Username:')
        register_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(300)
        register_layout.addWidget(self.username_input)

        password_label = QLabel('Password:')
        register_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        register_layout.addWidget(self.password_input)
        
        password_visibility_toggle = QCheckBox("Show password")
        password_visibility_toggle.stateChanged.connect(lambda: self.toggle_password_visibility(self.password_input, password_visibility_toggle))
        register_layout.addWidget(password_visibility_toggle)

        email_label = QLabel('Email:')
        register_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setFixedWidth(300)
        register_layout.addWidget(self.email_input)

        birthdate_label = QLabel('Birthdate:')
        register_layout.addWidget(birthdate_label)
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setFixedWidth(300)
        self.birthdate_input.setCalendarPopup(True)
        register_layout.addWidget(self.birthdate_input)

        register_button = QPushButton('Register')
        register_button.setFixedWidth(200)
        register_button.clicked.connect(self.register)
        register_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        login_button = QPushButton('Login Instead')
        login_button.setFixedWidth(200)
        login_button.clicked.connect(lambda: self.open_page("login"))
        login_button.setStyleSheet("border: none;")
        register_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        return register_layout


    async def window(self):
        w = self.widget
        l = self.layout  # Create a QVBoxLayout instance
        w.setWindowTitle("Planck | register")
        self.update_theme()

        tlayout = await self.title_layout()
        l.addLayout(tlayout)

        register_layout = self.register_layout()
        l.addLayout(register_layout)

        nav_layout = await self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

