import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import PyQt5

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

homepage_path = 'Homepage.html'

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

class customWebView(QWebEngineView):

    def closeEvent(self, event):
        # do stuff
        if True:
            event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            sys.exit()

    def loadUrl(self, url):
        self.setWindowState(Qt.WindowMaximized)
        self.load(QUrl(url))
        self.show()
        self.activateWindow()
        sys.exit(app.exec_())

class CustomWebBrowser(QMainWindow):
    global homepage_path
    def __init__(self, whitelist = [homepage_path, 'http://www.neopets.com/', 'http://www.coolmathgames.com/', 'http://www.ixl.com/', 'http://mail.google.com/'], url=homepage_path):
        super().__init__()
        self.mouse_widget = QtWidgets.QWidget()
        self.whitelist = whitelist or []
        self.init_ui()
        url = homepage_path
        if url:
            self.load_url(url)

    def init_ui(self):
        self.setWindowTitle("Custom Web Browser")
        self.setGeometry(0, 0, 800, 600)

        # Set up the main widget and layout
        main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # Set up the address bar
        address_bar = QtWidgets.QLineEdit(self)
        address_bar.returnPressed.connect(self.handle_address_entered)
        main_layout.addWidget(address_bar)

        # Set up the web view
        self.web_view = customWebView()
        self.web_view.loadStarted.connect(self.handle_load_started)
        self.web_view.loadProgress.connect(self.handle_load_progress)
        self.web_view.loadFinished.connect(self.handle_load_finished)
        main_layout.addWidget(self.web_view)

        # Load the homepage
        self.load_homepage()

    def load_homepage(self):
        self.load_url(homepage_path)

    def handle_address_entered(self):
        url = self.sender().text()
        self.load_url(url)

    def handle_load_started(self):
        self.statusBar().showMessage("Loading...")

    def handle_load_progress(self, progress):
        self.statusBar().showMessage("Loading... {}%".format(progress))

    def handle_load_finished(self):
        url = self.web_view.url().toString()
        self.statusBar().showMessage("Loaded: {}".format(url))

    def load_url(self, url):
        if self.is_allowed(url):
            self.web_view.loadUrl(url)
        else:
            self.statusBar().showMessage("Blocked: {}".format(url))

    def is_allowed(self, url):
        for allowed_url in self.whitelist:
            if url.startswith(allowed_url):
                return True
        return False

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

    def init_ui(self):
        self.setWindowTitle('Custom Web Browser')
        self.setGeometry(0, 0, 1080, 1080)

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
        self.text_layout = QVBoxLayout()
        self.sallie_entry = QLineEdit(self)
        self.sallie_entry.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.sallie_entry.setPlaceholderText('Sallie')
        self.text_layout.addWidget(self.sallie_entry, alignment=Qt.AlignTop)

        self.user_entry = QLineEdit(self)
        self.user_entry.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.user_entry.setPlaceholderText('User')
        self.text_layout.addWidget(self.user_entry, alignment=Qt.AlignTop)

        # Set the layout of the text boxes
        self.text_widget = QWidget()
        self.text_widget.setLayout(self.text_layout)
        self.text_widget.setMinimumWidth(300)

        # Create chat history box
        self.chat_history = QTextEdit(self)
        self.chat_history.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.chat_history.setReadOnly(True)
        self.chat_history.setMinimumHeight(100)

        # Set the main layout of the window
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.text_widget)
        self.main_layout.addWidget(self.chat_history)

        # Set the central widget and main layout of the window
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Create virtual mouse cursor
        self.mouse_cursor = QWidget(self.web_view)
        self.mouse_cursor.setFixedSize(20, 20)
        self.mouse_cursor.setStyleSheet('background-color: red; border-radius: 10px;')


        # Create virtual mouse scroll wheel
        self.scroll_wheel = QWidget(self.web_view)
        self.scroll_wheel.setFixedSize(20, 40)
        self.scroll_wheel.setStyleSheet('background-color: blue; border-radius: 10px;')


        # Create virtual keyboard
        self.keyboard = QWidget(self.web_view)
        self.keyboard.setFixedSize(300, 150)
        self.keyboard.setStyleSheet('background-color: #222;')

        # Create virtual keyboard buttons
        keyboard_layout = QGridLayout()
        self.keyboard.setLayout(keyboard_layout)

        buttons = [                '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=',     'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']',     'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'",     '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',     'shift', 'space', 'enter',    'left', 'up', 'down', 'right']

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
        buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", '\\', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'shift', 'space', 'enter', 'left', 'up', 'down', 'right']

        # check for shift key press and modify pressed key accordingly
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = True
            return

        # check for directional keys press
        if event.key() in [Qt.Key_Left, Qt.Key_Up, Qt.Key_Right, Qt.Key_Down]:
            # Handle directional key press
            pass

        # Handle other key presses
        if event.text() in buttons:
            if self.shift_pressed and event.text().isalpha():
                # handle uppercase letter press
                modified_text = event.text().upper()
            else:
                modified_text = event.text()
            # handle other key press
            pass

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = False

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
        super(CustomWebBrowser, self).show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.show()
    sys.exit(app.exec_())