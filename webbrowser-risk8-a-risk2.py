import os
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5 import QtGui
homepage_path = ('Homepage.html')

class ChatHistory(QDialog):
    def __init__(self, chat_history):
        super().__init__()
        self.setWindowTitle('Chat History')
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.chat_history = chat_history
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.chat_history)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

class CustomWebBrowser(QMainWindow):
    global homepage_path
    def __init__(self, whitelist = [homepage_path, 'https://www.neopets.com/', 'https://www.coolmathgames.com/', 'https://www.ixl.com/', 'https://mail.google.com/'], url=homepage_path):
        super().__init__()
        self.mouse_widget = PyQt5.QtWidgets.QWidget()
        self.whitelist = whitelist or []
        self.init_ui()
        if url:
            self.load_url(url)

    def load_url(self, url):
        self.web_view.load(QUrl(url))

    def release_chat(self):
        # Get the position of the Sallie chat window
        sallie_rect = self.web_view.page().mainFrame().findFirstElement('.user-message .sallie').geometry()

        # Calculate the position of the end of the bottom line
        x = sallie_rect.x() + sallie_rect.width() - 5
        y = sallie_rect.y() + sallie_rect.height() - 5

        # Move the mouse cursor to the position and click
        self.mouse_cursor.move(x, y)
        self.mouse_cursor.show()
        self.mouse_cursor.click()
        self.mouse_cursor.hide()


    def init_ui(self):
        self.setWindowTitle('Custom Web Browser')
        self.setGeometry(50, 50, 1080, 1080)

        # Create web view
        self.web_view = QWebEngineView(self)
        self.setCentralWidget(self.web_view)

        # Create toolbar
        self.toolbar = QToolBar(self)
        self.addToolBar(self.toolbar)

        # Create back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(self.web_view.back)
        self.toolbar.addAction(back_button)

        # Create forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(self.web_view.forward)
        self.toolbar.addAction(forward_button)

        # Create reload button
        reload_button = QAction('Reload', self)
        reload_button.triggered.connect(self.web_view.reload)
        self.toolbar.addAction(reload_button)

        # Create release button
        release_button = QPushButton('Release', self)
        release_button.setStyleSheet('background-color: #800080; color: white; font-size: 16px; font-weight: bold')
        release_button.clicked.connect(self.release_chat)
        self.toolbar.addWidget(release_button)

        # Create chat history button
        history_button = QPushButton('Chat History', self)
        history_button.setStyleSheet('background-color: #800080; color: white; font-size: 16px; font-weight: bold')
        history_button.clicked.connect(lambda: ChatHistory(self.chat_history.toPlainText()))
        self.toolbar.addWidget(history_button)

        # Create text boxes
        self.text_layout = QHBoxLayout()
        self.sallie_entry = QLineEdit(self)
        self.sallie_entry.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.sallie_entry.setPlaceholderText('Sallie')
        self.text_layout.addWidget(self.sallie_entry)
        self.user_entry = QLineEdit(self)
        self.user_entry.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.user_entry.setPlaceholderText('User')
        self.text_layout.addWidget(self.user_entry)

        # Create chat history box
        self.chat_history = QTextEdit(self)
        self.chat_history.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.chat_history.setReadOnly(True)
        self.chat_history.setMinimumHeight(100)

        # Create virtual mouse cursor
        self.mouse_cursor = QWidget(self.web_view)
        self.mouse_cursor.setFixedSize(20, 20)
        self.mouse_cursor.setStyleSheet('background-color: red; border-radius: 10px;')
        self.mouse_cursor.hide()

        # Create virtual mouse scroll wheel
        self.scroll_wheel = QWidget(self.web_view)
        self.scroll_wheel.setFixedSize(20, 40)
        self.scroll_wheel.setStyleSheet('background-color: blue; border-radius: 10px;')
        self.scroll_wheel.hide()

        # Create virtual keyboard
        self.keyboard = QWidget(self.web_view)
        self.keyboard.setFixedSize(300, 150)
        self.keyboard.setStyleSheet('background-color: #222;')

        # Create virtual keyboard buttons
        keyboard_layout = QGridLayout()
        self.keyboard.setLayout(keyboard_layout)

        buttons = [            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",            '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',            'shift', 'space', 'enter'        ]

        row = 0
        col = 0
        for button in buttons:
            button_widget = QPushButton(button)
            button_widget.setFixedSize(30, 30)
            button_widget.setStyleSheet('background-color: #333; color: white; border: none;')
            button_widget.clicked.connect(self.keyboard_button_clicked)
            keyboard_layout.addWidget(button_widget, row, col)

            col += 1
            if col > 12:
                row += 1
                col = 0

        self.keyboard.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scroll_wheel.show()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.scroll_wheel.hide()

    def wheelEvent(self, event):
        num_degrees = event.angleDelta().y() / 8
        num_steps = num_degrees / 15
        self.web_view.page().scroll(0, num_steps * 40)

    def keyboard_button_clicked(self):
        button = self.sender().text()
        if button == 'enter':
            self.web_view.page().runJavaScript('document.activeElement.blur();')
        elif button == 'space':
            self.web_view.page().runJavaScript('document.activeElement.value += " ";')
        elif button == 'shift':
            self.keyboard_shift = not self.keyboard_shift
            for i in range(self.keyboard.layout().count()):
                button = self.keyboard.layout().itemAt(i).widget()
                text = button.text()
                if len(text) == 1 and text.isalpha():
                    if self.keyboard_shift:
                        text = text.upper()
                    else:
                        text = text.lower()
                    button.setText(text)
        else:
            self.web_view.page().runJavaScript(f'document.activeElement.value += "{button}";')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.keyboard.hide()
        elif event.key() == Qt.Key_Return:
            self.web_view.page().runJavaScript('document.activeElement.blur();')
        elif event.key() == Qt.Key_Space:
            self.web_view.page().runJavaScript('document.activeElement.value += " ";')
        elif event.key() == Qt.Key_Shift:
                    self.keyboard_shift = True
                    for i in range(self.keyboard.layout().count()):
                        button = self.keyboard.layout().itemAt(i).widget()
                        text = button.text()
                        if len(text) == 1 and text.isalpha():
                            if self.keyboard_shift:
                                text = text.upper()
                            else:
                                text = text.lower()
                            button.setText(text)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.keyboard_shift = False
            for i in range(self.keyboard.layout().count()):
                button = self.keyboard.layout().itemAt(i).widget()
                text = button.text()
                if len(text) == 1 and text.isalpha():
                    text = text.lower()
                    button.setText(text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.width()
        height = self.height()

        # Position virtual mouse
        mouse_width = self.mouse_widget.width()
        mouse_height = self.mouse_widget.height()
        mouse_x = (width - mouse_width) // 2
        mouse_y = (height - mouse_height) // 2
        self.mouse_widget.move(mouse_x, mouse_y)

        # Position virtual scroll wheel
        scroll_width = self.scroll_wheel.width()
        scroll_height = self.scroll_wheel.height()
        scroll_x = width - scroll_width - 10
        scroll_y = (height - scroll_height) // 2
        self.scroll_wheel.move(scroll_x, scroll_y)

        # Position virtual keyboard
        keyboard_width = self.keyboard.width()
        keyboard_height = self.keyboard.height()
        keyboard_x = (width - keyboard_width) // 2
        keyboard_y = height - keyboard_height - 10
        self.keyboard.move(keyboard_x, keyboard_y)

        def show(self):
            self.resize(1080, 1080)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.showNormal()
    sys.exit(app.exec_())
