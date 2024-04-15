from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon, QFont, QBitmap, QPainter, QBrush
from PyQt5.QtCore import Qt, QSize
from qasync import QEventLoop, asyncSlot

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QApplication, QWidget
    from ..Planck import Application

WHITE = "#ffffff"
BLACK = "#333333" # very dark grey

CSS = {
    "theme": "background-color: {bgcolor}; color: {color};",
    "anti_theme": "background-color: {color}; color: {bgcolor};",
    "submit_button": "border: none; background-color: {color}; color: {bgcolor}; padding: 5px; border-radius: 10px;",
    "anti_submit_button": "border: none; background-color: {bgcolor}; color: {color}; padding: 5px; border-radius: 10px;",
    "input": "border: none; background-color: {bgcolor}; color: {color}; padding: 5px; border-radius: 10px;",
    "anti_input": "border: none; background-color: {color}; color: {bgcolor}; padding: 5px; border-radius: 10px;",
}

class Page:
    def __init__(self, app: Application):
        self.app: Application = app
        self.loop: QEventLoop = app.loop
        self.qapp: QApplication = app.qapp
        self.widget: QWidget = app.widget
        self.layout: QVBoxLayout | QHBoxLayout = app.layout
        self.layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.layout)

    def image(self, pc: str, callback=None, content = False):
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
        if content == True:
            pixmap = QPixmap()
            pixmap.loadFromData(pc)
        else:
            pixmap = QPixmap(pc)
        button.setIcon(QIcon(pixmap))
        button.setIconSize(pixmap.rect().size())
        if callback:
            button.clicked.connect(callback)
        return button, pixmap

    def create_circular_pixmap(self, pixmap):
        if pixmap.isNull() or pixmap.size().isEmpty():
            return pixmap
        
        size = pixmap.size()
        scaled_pixmap = pixmap.scaled(size * 4, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        mask = QBitmap(scaled_pixmap.size())
        mask.fill(Qt.color0)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.color1))
        painter.drawEllipse(scaled_pixmap.rect())
        painter.end()

        scaled_pixmap.setMask(mask)

        return scaled_pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def get_css(self, key: str) -> str:
        theme = self.app.theme
        bgcolor = WHITE if theme == 0 else BLACK
        color = BLACK if theme == 0 else WHITE
        return CSS.get(key).format(bgcolor=bgcolor,color=color,theme=theme)

    async def title_layout(self):  
        title = QPushButton("Planck")
        title.setFont(QFont('Arial', 20))
        title.setStyleSheet("border: none;")

        icon_size = 50
        title.setIcon(QIcon(QPixmap(self.app.icon_path)))
        title.setIconSize(QSize(icon_size, icon_size))

        title.clicked.connect(lambda: self.app.loop.create_task(self.open_page("home")))

        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addStretch(1)

        search_bar = self.search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search")
        search_bar.setStyleSheet(self.get_css("anti_input"))
        search_bar.setMinimumSize(200, 40)
        layout.addWidget(search_bar)

        search_button = QPushButton("🔍")
        search_button.setStyleSheet(self.get_css("anti_submit_button"))
        search_button.clicked.connect(lambda: self.open_page("search"))
        search_button.setFont(QFont('Arial', 20))
        layout.addWidget(search_button)
        layout.addStretch(1)

        acc = self.app.http.account
        if acc:
            if len(acc['pfp']) > 0:
                purl = 'cdn/pfp/' + acc['pfp']
                p = await self.app.http.fetch_image(purl)
                profile_button, pixmap = self.image(p, lambda: self.open_page("profile"), content=True)
                pixmap = self.create_circular_pixmap(pixmap)
                profile_button.setIcon(QIcon(pixmap))
            else:
                profile_button, pixmap = self.image(self.app.icon_path, lambda: self.open_page("profile"))
                pixmap = self.create_circular_pixmap(pixmap)
                profile_button.setIcon(QIcon(pixmap))
            profile_button.setIconSize(QSize(icon_size, icon_size))
            profile_button.setText(acc['username'])
            profile_button.setStyleSheet(self.get_css("submit_button"))
            layout.addWidget(profile_button)

        return layout

    async def nav_layout(self):
        layout = QHBoxLayout()
        layout.addStretch(1)
        op = lambda page: (lambda: self.open_page(page))
        if self.app.http.account:
            for page in ('home', 'feed', 'settings'):
                button = QPushButton(page.capitalize())
                button.clicked.connect(op(page))
                button.setStyleSheet("border: none;")
                button.setFont(QFont('Arial', 20))
                button.setStyleSheet(self.get_css("submit_button"))
                layout.addWidget(button)
                layout.addStretch(1)
            lb = QPushButton("Logout")
            lb.setStyleSheet(self.get_css("submit_button"))
            lb.clicked.connect(self.app.http.logout)
            lb.setFont(QFont('Arial', 20))
            layout.addWidget(lb)
            layout.addStretch(1)
        else:
            for page in ('home', 'login', 'register'):
                button = QPushButton(page.capitalize())
                button.clicked.connect(op(page))
                button.setStyleSheet("border: none;")
                button.setFont(QFont('Arial', 20))
                button.setStyleSheet(self.get_css("submit_button"))
                layout.addWidget(button)
                layout.addStretch(1)
        return layout

    def update_theme(self):
        self.widget.setStyleSheet(self.get_css("theme"))


    @asyncSlot()
    async def open_page(self, page: str):
        """Open a page.

        Parameters
        ----------

        page:`str`
            The name of the page to open.
        """
        await self.clear_layout(self.layout)
        await self.app.pages[page].window()


    async def clear_layout(self, layout: QVBoxLayout | QHBoxLayout):
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

    async def reload(self):
        """Reload the page.
        """
        l = self.layout
        await self.clear_layout(l)
        await self.window()

