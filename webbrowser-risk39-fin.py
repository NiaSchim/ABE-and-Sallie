import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import PyQt5
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtQml import QJSValue
import json
from jinja2 import Environment, FileSystemLoader
from jinja2 import Template

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# Set the current working directory to the directory where the current module is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Use a relative path for the homepage_path
homepage_path = 'Homepage.html'
popup_template_path = 'popup_template.html'

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
    global popup_template_path  # Added global variable for the Jinja2 template
    global homepage_path
    def __init__(self, whitelist=[homepage_path, 'http://www.neopets.com/', 'http://www.coolmathgames.com/', 'http://www.ixl.com/', 'http://mail.google.com/'], url=homepage_path):
        super().__init__()

        # Set window properties
        self.setWindowTitle("AGI Browser Environment (ABE)")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setMinimumSize(600, 400)
        self.setFixedSize(600, 400)  # Increase window size by 1/4th

        # Set up the central widget
        self.central_widget = QtWidgets.QWidget(self)

        # Create a layout for the central widget
        self.central_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # Create a vertical layout for the address bar, buttons, and web view
        self.left_layout = QtWidgets.QVBoxLayout()

        # Add the left layout to the central layout
        self.central_layout.addLayout(self.left_layout)

        # Create a horizontal layout for the address bar and buttons
        self.address_layout = QtWidgets.QHBoxLayout()

        # Add the address layout to the left layout
        self.left_layout.addLayout(self.address_layout)

        # Create a QWebEngineView widget
        self.web_view = QWebEngineView()  # Define web_view as an instance variable

        # Use QUrl.fromLocalFile to load the local HTML file
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(url)))

        # Create a QWebChannel to communicate between JavaScript and Python
        self.web_channel = QWebChannel()
        self.web_view.page().setWebChannel(self.web_channel)
        self.web_channel.registerObject("browser", self)

        # Add the web_view to the left layout
        self.left_layout.addWidget(self.web_view)

        # Home button
        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.go_home)
        self.address_layout.addWidget(self.home_button)

        # Add back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.web_view.back)
        self.address_layout.addWidget(self.back_button)

        # Add forward button
        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.web_view.forward)
        self.address_layout.addWidget(self.forward_button)

        # Add chat history button
        self.chat_history_button = QPushButton("Chat History")
        self.chat_history_button.clicked.connect(self.open_chat_history)
        self.address_layout.addWidget(self.chat_history_button)

        # Set up AI chat panel
        self.ai_chat_panel = QVBoxLayout()
        self.central_layout.addLayout(self.ai_chat_panel)

        # AI message box (to be controlled by AI)
        self.ai_message_box = QTextEdit()
        self.ai_message_box.setReadOnly(True)  # Placeholder for AI-controlled typing
        self.ai_message_box.setFixedHeight(self.height() // 3)
        self.ai_chat_panel.addWidget(self.ai_message_box)

        # Release button
        self.release_button = QPushButton("Release")
        self.release_button.clicked.connect(self.release_ai)
        self.ai_chat_panel.addWidget(self.release_button)

        # User input box
        self.user_input_box = QLineEdit()
        self.user_input_box.setFixedHeight(self.height() // 3)
        self.user_input_box.setPlaceholderText("Send message to AI")
        self.user_input_box.returnPressed.connect(self.send_message_to_ai)
        self.ai_chat_panel.addWidget(self.user_input_box)

        # Set the central_widget as the central widget of the QMainWindow
        self.setCentralWidget(self.central_widget)

    def go_home(self):
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(homepage_path)))
        self.inject_javascript()

    def send_message_to_ai(self):
        user_message = self.user_input_box.text()
        if user_message:
            with open("chat-history.txt", "a") as chat_history:
                chat_history.write(f"User: {user_message}\n")
            self.user_input_box.clear()
            self.ai_message_box.setPlainText("AI: Placeholder response")

    def release_ai(self):
        pass

    def open_chat_history(self):
        chat_history_file = "chat-history.txt"
        chat_history = ""

        try:
            with open(chat_history_file, "a+") as file:
                file.seek(0)
                chat_history = file.read()
        except IOError as e:
            print(f"Error opening chat history file: {e}")

        self.chat_history_window = ChatHistory(chat_history)
        self.chat_history_window.show()

    # New method to load stored credentials
    def load_credentials(self):
        try:
            with open("credentials.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    # New method to save stored credentials
    def save_credentials(self, credentials):
        with open("credentials.json", "w") as f:
            json.dump(credentials, f)

    # New method to render the popup.html file using Jinja2
    def render_popup(self):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(popup_template_path)

        rendered_html = template.render(credentials=self.credentials)

        with open('popup.html', 'w') as f:
            f.write(rendered_html)


    # New method to add new credentials to the list and update the popup.html file
    def add_credentials(self, website_name, url, username, password):
        new_credential = {
            "website_name": website_name,
            "url": url,
            "username": username,
            "password": password
        }
        self.credentials.append(new_credential)
        self.save_credentials(self.credentials)
        self.render_popup()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.show()
    sys.exit(app.exec_())
