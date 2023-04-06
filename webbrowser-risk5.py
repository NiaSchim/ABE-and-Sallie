import os
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class CustomWebBrowser(QMainWindow):
    def __init__(self, whitelist=None):
        super().__init__()
        self.whitelist = whitelist or []
        self.init_ui()

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
        history_button.clicked.connect(self.show_chat_history)
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

        # Add text boxes and chat history box to layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.text_layout)
        self.layout.addWidget(self.chat_history)

        # Create main widget and set layout
        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.layout)

        # Set main widget as central widget
        self.setCentralWidget(self.main_widget)

        # Connect text boxes to web view
        self.user_entry.returnPressed.connect(self.send_user_message)
        self.sallie_entry.returnPressed.connect(self.send_sallie_message)

        # Load homepage
        homepage_path = 'Homepage.html'
        if os.path.exists(homepage_path):
            url = QUrl.fromLocalFile(os.path.abspath(homepage_path))
            self.web_view.load(url)
        else:
            print(f"{homepage_path} not found")
            self.web_view.setHtml("<h1>Homepage not found</h1>")

    def send_user_message(self):
        user_message = self.user_entry.text()
        self.add_message_to_chat(user_message, is_user=True)
        self.send_message_to_sallie(user_message)
        self.user_entry.clear()

    def send_sallie_message(self):
        sallie_message = self.sallie_entry.text()
        self.add_message_to_chat(sallie_message, is_user=False)
        self.sallie_entry.clear()

    def send_message_to_sallie(self, message):
        response = generate_response(message)
        self.add_message_to_chat(response, is_user=False)

    def add_message_to_chat(self, message, is_user=True):
        if is_user:
            message_box = self.user_message_box
            message_class = "user-message"
        else:
            message_box = self.sallie_message_box
            message_class = "sallie-message"

        message_html = f"<div class='{message_class}'>{message}</div>"
        message_box.append(message_html)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomWebBrowser()
    window.show()
    sys.exit(app.exec_())

