from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QSize

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QApplication, QWidget
    from ..Planck import Application

class Page:
    def __init__(self, app: Application):
        self.app: Application = app
        self.qapp: QApplication = app.qapp
        self.widget: QWidget = app.widget
        self.layout: QVBoxLayout | QHBoxLayout = app.layout
        self.layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.layout)
    

    def image(self, path: str, callback=None):
        """Display an image on the page.

        Parameters
        ----------
        path:`str`
            The path to the image file.

        Returns
        -------
        `Tuple`[`QPushButton`, `QPixmap`]
            Tuple containing the QPushButton and QPixmap objects.
        """
        button = QPushButton()
        if path.startswith(("http://", "https://")):
            pixmap = QPixmap()
            pixmap.loadFromData(self.app.http.get(path).content)
        else:
            pixmap = QPixmap(path)
        button.setIcon(QIcon(pixmap))
        button.setIconSize(pixmap.rect().size())
        if callback:
            button.clicked.connect(callback)
        return button, pixmap

    def title_layout(self):  
        title = QPushButton("Planck")
        title.setFont(QFont('Arial', 30))
        title.clicked.connect(lambda: self.open_page("home"))
        title.setStyleSheet("border: none;")

        icon_size = title.font().pointSize()
        ibut, pixmap = self.image(self.app.icon_path, lambda: self.open_page("home"))
        ibut.setIconSize(QSize(icon_size, icon_size))
        ibut.setStyleSheet("border: none;")

        purl = self.app.http.account['pfp'] if self.app.http.account else self.app.icon_path
        profile_button, profile_pixmap = self.image(purl, lambda: self.open_page("profile"))
        profile_button.setIconSize(QSize(icon_size, icon_size))
        profile_button.setStyleSheet("border: none;")

        layout = QHBoxLayout()
        layout.addWidget(ibut)
        layout.addWidget(title)
        layout.addStretch(1)
        layout.addWidget(profile_button)

        return layout

    def nav_layout(self):
        layout = QHBoxLayout()
        layout.addStretch(1)
        op = lambda page: (lambda: self.open_page(page))
        for page in self.app.pages:
            button = QPushButton(page.capitalize())
            button.clicked.connect(op(page))
            button.setStyleSheet("border: none;")
            button.setFont(QFont('Arial', 15))
            layout.addWidget(button)
            layout.addStretch(1)
        return layout

    def open_page(self, page: str):
        """Open a page.

        Parameters
        ----------

        page:`str`
            The name of the page to open.
        """
        self.clear_layout(self.layout)
        self.app.pages[page].window()


    def clear_layout(self, layout: QVBoxLayout | QHBoxLayout):
        """Clear a layout.

        Parameters
        ----------
        layout:`QVBoxLayout | QHBoxLayout`
        """
        while layout.count():
            child = layout.takeAt(0)
            widget = child.widget()
            if widget is not None:
                widget.setParent(None)
            elif child.layout() is not None:
                while child.layout().count():
                    sub_child = child.layout().takeAt(0)
                    if sub_child.widget() is not None:
                        sub_child.widget().setParent(None)

    def reload(self):
        """Reload the page.
        """
        l = self.layout
        self.clear_layout(l)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.layout)
        self.window()

