__all__ = ("Login",)

from typing import List, Dict, Any

import json

from .base import Page

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qasync import asyncSlot

class Login(Page):
    """The login page.
    """
    NAME = "register"

    def __init__(
        self,
        app
    ):
        super().__init__(app)

    def login(self):
        async def _internal():
            username = self.username_input.text()
            password = self.password_input.text()
            u = await self.app.http.login(username, password)
            if u:
                self.app.http.accounts[u['api_key']] = u
                self.app.http.account = u
                with open("cache.json", "w") as f:
                    json.dump({"accounts": self.app.http.accounts, "account": u, "theme": self.app.theme}, f)
                await self.clear_layout(self.layout)
                await self.app.pages['home'].window()
        self.app.loop.create_task(_internal())

    def login_layout(self):
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)

        username_label = QLabel('Username or Email:')
        login_layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(300)
        login_layout.addWidget(self.username_input)

        password_label = QLabel('Password:')
        login_layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        login_layout.addWidget(self.password_input)
        
        password_visibility_toggle = QCheckBox("Show password")
        password_visibility_toggle.stateChanged.connect(lambda: self.toggle_password_visibility(self.password_input, password_visibility_toggle))
        login_layout.addWidget(password_visibility_toggle)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        login_button.setFixedWidth(200)
        login_layout.addWidget(login_button,  alignment=Qt.AlignCenter)

        register_button = QPushButton('Register Instead')
        register_button.clicked.connect(lambda: self.open_page("register"))
        register_button.setFixedWidth(200)
        register_button.setStyleSheet("border: none;")
        login_layout.addWidget(register_button,  alignment=Qt.AlignCenter)

        return login_layout

    def toggle_password_visibility(self, password_input, checkbox):
        if checkbox.isChecked():
            password_input.setEchoMode(QLineEdit.Normal)
        else:
            password_input.setEchoMode(QLineEdit.Password)

    async def window(self):
        w = self.widget
        l = self.layout  # Create a QVBoxLayout instance
        w.setWindowTitle("Planck | Login")
        self.update_theme()

        tlayout = await self.title_layout()
        l.addLayout(tlayout)

        login_layout = self.login_layout()
        l.addStretch(1)
        l.addLayout(login_layout)

        nav_layout = await self.nav_layout()
        l.addStretch(1)
        l.addLayout(nav_layout)

        w.show()

