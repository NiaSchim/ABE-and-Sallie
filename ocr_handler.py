import subprocess
import sys
import pytesseract
from PIL import Image
import pygetwindow as gw
import pyautogui

def is_tesseract_installed():
    try:
        subprocess.run(["tesseract", "-v"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def prompt_tesseract_installation():
    print("Tesseract OCR is not installed on your system.")
    print("Please install it from the following website:")
    print("https://tesseract-ocr.github.io/tessdoc/Downloads.html")
    sys.exit(1)

def extract_text_from_window(window_title):
    if not is_tesseract_installed():
        prompt_tesseract_installation()

    try:
        # Get the window by its title
        window = gw.getWindowsWithTitle(window_title)[0]
    except IndexError:
        print(f"Window with title '{window_title}' not found.")
        return None, None

    # Capture the window's content
    screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))

    # Run OCR using Tesseract and get data
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    # Extract text and bounding boxes
    text = []
    bounding_boxes = []
    for i in range(len(data["level"])):
        if data["level"][i] == 5:  # Word level
            text.append(data["text"][i])
            bounding_boxes.append((data["left"][i], data["top"][i], data["width"][i], data["height"][i]))

    return text, bounding_boxes