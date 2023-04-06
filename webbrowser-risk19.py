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
        self.setMinimumSize(800, 600)
        self.setFixedSize(1080, 1080)

        # Set up the central widget
        self.central_widget = QtWidgets.QWidget(self)

        # Create a layout for the central widget
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Create a horizontal layout for the address bar and buttons
        self.address_layout = QtWidgets.QHBoxLayout()

        # Add the address layout to the central layout
        self.central_layout.addLayout(self.address_layout)

        # Create a QWebEngineView widget
        self.web_view = QWebEngineView() # Define web_view as an instance variable

        # Use QUrl.fromLocalFile to load the local HTML file
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(url)))

        # Add the web_view to the central layout
        self.central_layout.addWidget(self.web_view)

        # Set the central_widget as the central widget of the QMainWindow
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.show()
    sys.exit(app.exec_())