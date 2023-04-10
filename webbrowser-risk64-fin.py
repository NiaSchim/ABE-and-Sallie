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
import datetime
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
import time
import threading
from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from PyQt5.QtWidgets import QMenu, QAction, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
from pynput import mouse, keyboard
import pyautogui
import math
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
import webview
from PyQt5.QtCore import QSize

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# Set the current working directory to the directory where the current module is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Use a relative path for the homepage_path
homepage_path = 'Homepage.html'

def map_button_arg(button):
    button_map = {
        "Button.left": "left",
        "Button.middle": "middle",
        "Button.right": "right"
    }
    return button_map.get(button, "left")

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

class RecordingButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(RecordingButton, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.customContextMenuRequested.emit(event.pos())
        else:
            super(RecordingButton, self).mousePressEvent(event)

class CustomCursor:
    def __init__(self, cursor_image_path):
        self.cursor_image = QImage(cursor_image_path)
        self.cursor = QCursor(QPixmap.fromImage(self.cursor_image))


class CustomWebBrowser(QMainWindow):
    def __init__(self, whitelist=[homepage_path, 'http://www.neopets.com/', 'http://www.coolmathgames.com/', 'http://www.ixl.com/', 'http://mail.google.com/'], url=homepage_path):
        super().__init__()

        # Set window properties
        self.setWindowTitle("AGI Browser Environment (ABE)")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setMinimumSize(600, 400)
        self.setFixedSize(600, 400)

        # Create a QWindow to host the PyWebView window
        self.web_window = QWindow()
        self.web_window.setMinimumSize(QSize(600, 400))

        # Set window flag to remove all standard window buttons
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint)

        # Create a QWidget to host the QWindow
        self.web_widget = QWidget.createWindowContainer(self.web_window, self)

        # Set the size to 1 pixel by 1 pixel
        self.web_widget.setFixedSize(1, 1)

        # Hide the widget
        self.web_widget.hide()

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
        self.web_view = QWebEngineView()

        # Configure QWebEngineProfile for better compatibility
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)

        # Create and set a custom QWebEnginePage with the configured profile
        custom_page = QWebEnginePage(profile, self.web_view)
        self.web_view.setPage(custom_page)

        # Set the QWebEngineView settings attributes
        settings = self.web_view.page().settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)

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

        # Add recording button
        self.recording_button = RecordingButton("Start Recording")
        self.address_layout.addWidget(self.recording_button)

        # Create a list to hold the recordings
        self.recordings = []

        # Create a list to hold the current recording
        self.current_recording = []

        # Create a boolean to keep track of whether recording is currently in progress
        self.recording = False

        self.recordings_menu = QMenu(self)
        self.recording_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.recording_button.customContextMenuRequested.connect(self.show_recordings_menu)
        self.recording_button.clicked.connect(self.toggle_recording)

    def mimic_input(self, event):
        try:
            if event["type"] == "mousemove":
                pyautogui.moveTo(event["x"], event["y"])
            elif event["type"] == "click":
                button = event["button"]
                if button == "Button.left":
                    pyautogui.click(x=event["x"], y=event["y"], button="left")
                elif button == "Button.right":
                    pyautogui.click(x=event["x"], y=event["y"], button="right")
                elif button == "Button.middle":
                    pyautogui.click(x=event["x"], y=event["y"], button="middle")
            elif event["type"] == "keydown":
                key = event["key"]
                pyautogui.press(key)
            elif event["type"] == "scroll":
                pyautogui.scroll(event["dy"])
        except Exception as e:
            print(f"Error: {e}")
            print(f"Event: {event}")  # Print the event dictionary when an error occurs

    # Add this function to record the scroll wheel events
    def on_scroll(self, x, y, dx, dy):
        if self.recording:
            self.current_recording.append({"type": "scroll", "timestamp": datetime.datetime.now(), "x": x, "y": y, "dx": dx, "dy": dy})

    def show_recordings_menu(self):
        if not self.recording:
            self.load_recordings()
            self.recordings_menu.setFixedWidth(200)  # Set the fixed width for the recordings menu
            self.recordings_menu.exec_(self.recording_button.mapToGlobal(QtCore.QPoint(0, self.recording_button.height()))) # Set the fixed width for the recordings menu

    def toggle_recording(self):
        if not self.recording:
            self.recording_button.setText("Stop Recording")
            self.recording = True
            self.current_recording = []

            def on_move(x, y):
                global_pos = QPoint(x, y)
                local_pos = self.web_view.mapFromGlobal(global_pos)
                self.current_recording.append({"type": "mousemove", "x": local_pos.x(), "y": local_pos.y(), "timestamp": datetime.datetime.now().isoformat()})

            def on_click(x, y, button, pressed):
                if pressed:
                    global_pos = QPoint(x, y)
                    local_pos = self.web_view.mapFromGlobal(global_pos)
                    self.current_recording.append({"type": "click", "x": local_pos.x(), "y": local_pos.y(), "button": str(button), "timestamp": datetime.datetime.now().isoformat()})

            def on_scroll(x, y, dx, dy):
                global_pos = QPoint(x, y)
                local_pos = self.web_view.mapFromGlobal(global_pos)
                self.current_recording.append({"type": "scroll", "x": local_pos.x(), "y": local_pos.y(), "dx": dx, "dy": dy, "timestamp": datetime.datetime.now().isoformat()})

            def on_press(key):
                try:
                    key_char = key.char
                except AttributeError:
                    key_char = str(key)
                self.current_recording.append({"type": "keydown", "key": key_char, "timestamp": datetime.datetime.now().isoformat()})

            self.mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
            self.keyboard_listener = keyboard.Listener(on_press=on_press)
            self.mouse_listener.start()
            self.keyboard_listener.start()
        else:
            self.recording_button.setText("Start Recording")
            self.recording = False
            self.mouse_listener.stop()
            self.keyboard_listener.stop()

            recording_name, ok = QInputDialog.getText(self, "Recording Name", "Enter a name for the recording:")
            if ok:
                current_webpage = self.web_view.url().toString()

                # Read existing recordings
                try:
                    with open("recordings.json", "r") as f:
                        self.recordings = json.load(f)
                except (IOError, json.JSONDecodeError):
                    self.recordings = []

                # Append the new recording
                self.recordings.append({"name": recording_name, "timestamp": datetime.datetime.now(), "events": self.current_recording, "webpage": current_webpage})

                # Save the updated list of recordings
                with open("recordings.json", "w") as f:
                    json.dump(self.recordings, f, default=str)

    def filter_recordings_by_webpage(self, recordings, current_webpage):
        filtered_recordings = [r for r in recordings if r["webpage"] == current_webpage]
        return filtered_recordings

    def on_move(self, x, y):
        if self.recording:
            self.current_recording.append({"type": "mousemove", "timestamp": datetime.datetime.now(), "x": x, "y": y})

    def on_click(self, x, y, button, pressed):
        if self.recording and pressed:
            self.current_recording.append({"type": "click", "timestamp": datetime.datetime.now(), "x": x, "y": y, "button": str(button)})

    def on_press(self, key):
        if self.recording:
            self.current_recording.append({"type": "keydown", "timestamp": datetime.datetime.now(), "key": str(key)})

    def load_recordings(self):
        self.recordings_menu.clear()
        try:
            with open("recordings.json", "r") as f:
                self.recordings = json.load(f)
        except (IOError, json.JSONDecodeError):
            self.recordings = []

        current_webpage = self.web_view.url().toString()  # Get the current webpage URL
        recordings = self.filter_recordings_by_webpage(self.recordings, current_webpage)

        for recording in recordings:
            action = QAction(recording["name"], self)
            action.triggered.connect(lambda checked, r=recording: self.play_recording(r))
            self.recordings_menu.addAction(action)

    def play_recording(self, recording):
        cursor_image_path = "cursor_image.png"
        self.custom_cursor = CustomCursor(cursor_image_path)
        QApplication.setOverrideCursor(self.custom_cursor.cursor)

        def play_event(event_index, skip_mouse_moves=9):
            try:
                if event_index >= len(recording["events"]):
                    QApplication.restoreOverrideCursor()  # Show the actual cursor
                    return

                event = recording["events"][event_index]

                if event["type"] == "mousemove":
                    if skip_mouse_moves == 10:
                        local_pos = QPointF(float(event["x"]), float(event["y"]))
                        global_pos = self.web_view.mapToGlobal(local_pos.toPoint())
                        pyautogui.moveTo(global_pos.x(), global_pos.y())
                        skip_mouse_moves = 0
                    else:
                        skip_mouse_moves += 1
                elif event["type"] == "click":
                    local_pos = QPointF(float(event["x"]), float(event["y"]))
                    global_pos = self.web_view.mapToGlobal(local_pos.toPoint())
                    button_arg = map_button_arg(event["button"])
                    pyautogui.click(global_pos.x(), global_pos.y(), button=button_arg)
                elif event["type"] == "keydown":
                    pyautogui.press(event["key"])
                elif event["type"] == "scroll":
                    pyautogui.scroll(int(event["dy"]))
                else:
                    pass

                if event_index + 1 < len(recording["events"]):
                    next_event = recording["events"][event_index + 1]
                    if next_event["type"] == "mousemove":
                        QTimer.singleShot(0, lambda: play_event(event_index + 1, skip_mouse_moves))
                    else:
                        event_interval = (datetime.datetime.fromisoformat(next_event["timestamp"]) - datetime.datetime.fromisoformat(event["timestamp"])).total_seconds() * 1000
                        QTimer.singleShot(int(event_interval), lambda: play_event(event_index + 1, skip_mouse_moves))
                else:
                    QTimer.singleShot(1, QApplication.restoreOverrideCursor)  # Restore the cursor after a short delay
            except Exception as e:
                print(f"Error playing event: {e}")

        try:
            play_event(0)
        except Exception as e:
            print(f"Error initializing play_event: {e}")

    def go_home(self):
        self.web_view.setUrl(QUrl.fromLocalFile(os.path.abspath(homepage_path)))

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomWebBrowser()
    browser.show()
    sys.exit(app.exec_())
