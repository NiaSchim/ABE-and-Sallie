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

class CustomWebBrowser(QMainWindow):
    global homepage_path
    def __init__(self, whitelist = [homepage_path, 'http://www.neopets.com/', 'http://www.coolmathgames.com/', 'http://www.ixl.com/', 'http://mail.google.com/'], url=homepage_path):
        super().__init__()
        self.mouse_widget = QtWidgets.QWidget()
        self.whitelist = whitelist or []
        self.web_view = QWebEngineView() # Define web_view as an instance variable
        self.main_widget = QWidget(self)
        self.init_ui()

        self.loadUrl(url)

    def closeEvent(self, event):
        # do stuff
        if True:
            event.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            sys.exit()

    def loadUrl(self, url):
        self.setWindowState(Qt.WindowMaximized)
        self.web_view.setUrl(QUrl(url))
        self.show()
        self.activateWindow()

    def load_homepage(self):
        self.loadUrl(homepage_path)

    def handle_address_entered(self):
        url = self.sender().text()
        self.loadUrl(url)

    def handle_load_started(self):
        self.statusBar().showMessage("Loading...")

    def handle_load_progress(self, progress):
        self.statusBar().showMessage("Loading... {}%".format(progress))

    def handle_load_finished(self):
        url = self.web_view.url().toString()
        self.statusBar().showMessage("Loaded: {}".format(url))

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
        url_str = self.loadUrl(homepage_path)
        url = QtCore.QUrl(url_str)
        self.web_view = QtWebEngineWidgets.QWebEngineView()
        self.web_view.setUrl(url)
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
        history_button = QPushButton('Chat History')
        history_button.setStyleSheet('background-color: #800080; color: white; font-size: 16px; font-weight: bold')
        history_button.clicked.connect(self.show_chat_history)
        self.toolbar.addWidget(history_button)

        # Create chat input box
        self.chat_input = QLineEdit(self)
        self.chat_input.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.chat_input.setPlaceholderText('Enter your message here')
        self.chat_input.returnPressed.connect(self.send_chat)

        # Set the layout of the chat input box
        self.text_layout = QVBoxLayout()
        self.text_layout.addWidget(self.chat_input, alignment=Qt.AlignTop)
        self.text_widget = QWidget()
        self.text_widget.setLayout(self.text_layout)
        self.text_widget.setMinimumWidth(300)


    def show_chat_history(self):
        # Create chat history window
        self.chat_history_window = QMainWindow()
        self.chat_history_window.setWindowTitle('Chat History')

        # Create chat history text box
        self.chat_history_text_box = QTextEdit()
        self.chat_history_text_box.setStyleSheet('border: 2px solid #800080; font-size: 16px; font-weight: bold')
        self.chat_history_text_box.setReadOnly(True)
        self.chat_history_text_box.setMinimumHeight(100)

        # Set the chat history text box content
        if os.path.exists(chat_history_path):
            with open(chat_history_path, 'r') as f:
                chat_history = f.read()
                self.chat_history_text_box.setText(chat_history)

        # Add chat history text box to chat history window
        self.chat_history_window.setCentralWidget(self.chat_history_text_box)

        # Show chat history window
        self.chat_history_window.show()

        # Create chat history file if non-existent
        if not os.path.exists(chat_history_path):
            open(chat_history_path, 'w').close()

    def send_chat(self):
        # Append message to chat history file
        with open(chat_history_path, 'a') as f:
            f.write(self.chat_input.text() + '\n')

        # Clear chat input box
        self.chat_input.setText('')


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

    def show(self):
        super(CustomWebBrowser, self).show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.show()
    sys.exit(app.exec_())