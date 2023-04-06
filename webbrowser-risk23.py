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

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# Set the current working directory to the directory where the current module is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Use a relative path for the homepage_path
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
    def __init__(self, whitelist=[homepage_path, 'http://www.neopets.com/', 'http://www.coolmathgames.com/', 'http://www.ixl.com/', 'http://mail.google.com/'], url=homepage_path):
        super().__init__()

        # Set window properties
        self.setWindowTitle("AGI Browser Environment (ABE)")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setMinimumSize(600, 600)
        self.setFixedSize(600, 600)  # Increase window size by 1/4th

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
        self.ai_chat_panel.addWidget(self.ai_message_box)

        # User input box
        self.user_input_box = QLineEdit()
        self.user_input_box.setPlaceholderText("Send message to AI")
        self.user_input_box.returnPressed.connect(self.send_message_to_ai)
        self.ai_chat_panel.addWidget(self.user_input_box)

        # Release button
        self.release_button = QPushButton("Release")
        self.release_button.clicked.connect(self.release_ai)
        self.ai_chat_panel.addWidget(self.release_button)

        # Set the central_widget as the central widget of the QMainWindow
        self.setCentralWidget(self.central_widget)

    def go_home(self):
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(homepage_path)))

    def send_message_to_ai(self):
        user_message = self.user_input_box.text()
        if user_message:
            with open("chat-history.txt", "a") as chat_history:
                chat_history.write(f"User: {user_message}\n")
            self.user_input_box.clear()
            # TODO: Implement AI response logic
            self.ai_message_box.setPlainText("AI: Placeholder response")

    def release_ai(self):
        # TODO: Implement AI release logic
        pass

    def open_chat_history(self):
        chat_history_file = "chat-history.txt"
        chat_history = ""

        # Read or create the chat history file
        try:
            with open(chat_history_file, "a+") as file:
                file.seek(0)
                chat_history = file.read()
        except IOError as e:
            print(f"Error opening chat history file: {e}")

        # Display chat history in a new window
        self.chat_history_window = ChatHistory(chat_history)
        self.chat_history_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.show()
    sys.exit(app.exec_())
