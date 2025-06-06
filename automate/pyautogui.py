import cv2
import numpy as np
from PIL import Image
import pyautogui
from datetime import datetime
from time import sleep
from random import randint
import os

def generate_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_screen_size():
    return pyautogui.size()

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_run_folder(run_folder):
    os.makedirs(run_folder, exist_ok=True)

def log_action(context, action, outcome="👌"):
    data = f"[{outcome}] {get_current_datetime()} - {action}"
    print(data)
    with open(f"{context.get_run_folder()}/actions.log", "a", encoding="utf-8") as f:
        f.write(data + "\n")


class Click:
    def __init__(self, type="left", clicks=1, delay=0.1):
        self.type = type
        self.clicks = clicks
        self.delay = delay
    
    def execute(self, context):
        pyautogui.click(button=self.type, clicks=self.clicks, interval=self.delay)
        log_action(context, f"Clicked {self.type} {self.clicks} times with {self.delay} delay", "👆")

class DragTo:
    def __init__(self, x_ratio, y_ratio, duration=0.5):
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.duration = duration
    
    def execute(self, context):
        w, h = get_screen_size()
        x = round(self.x_ratio * w)
        y = round(self.y_ratio * h)
        pyautogui.dragTo(x, y, duration=self.duration)
        log_action(context, f"Dragged to {x}, {y} with {self.duration} duration", "👆")

class MouseMove:
    def __init__(self, x_ratio, y_ratio, duration=0.5):
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.duration = duration
    
    def execute(self, context):
        w, h = get_screen_size()
        x = round(self.x_ratio * w)
        y = round(self.y_ratio * h)
        pyautogui.moveTo(x, y, duration=self.duration)
        log_action(context, f"Moved mouse to {x}, {y} with {self.duration} duration", "👆")

class Screenshot:
    def __init__(self, delay=1):
        self.delay = delay

    def execute(self, context):
        sleep(self.delay)
        filename = f"{generate_timestamp()}.png"
        pyautogui.screenshot(f"{context.get_run_folder()}/{filename}")
        log_action(context, f"Took screenshot {filename}", "📷")

class TypeKeys:
    def __init__(self, keys):
        self.keys = keys

    def execute(self, context):
        pyautogui.typewrite(self.keys)
        log_action(context, f"Typed {self.keys}", "📝")

class Keys:
    def __init__(self, key_sequences):
        self.key_sequences = key_sequences if isinstance(key_sequences, list) else [key_sequences]
    
    def execute(self, context):
        for sequence in self.key_sequences:
            if isinstance(sequence, tuple):
                for key in sequence:
                    pyautogui.keyDown(key)
                for key in reversed(sequence):
                    pyautogui.keyUp(key)
            else:
                pyautogui.press(sequence)
        log_action(context, f"Pressed {self.key_sequences}", "🔄")

class Sleep:
    def __init__(self, duration=3, randomize=True):
        self.duration = duration
        self.randomize = randomize
    
    def execute(self, context):
        if self.randomize:
            min_duration = max(self.duration - 1, 1)
            sleep(randint(min_duration, self.duration))
        else:
            sleep(self.duration)
        log_action(context, f"Slept for {self.duration} seconds", "⏳")

class ClickOnReference:
    def __init__(self, reference_file, type="left", clicks=1, delay=0.1, duration=0.1):
        self.reference_path = f"./assertions/{reference_file}.png" 
        self.type = type
        self.clicks = clicks
        self.delay = delay
        self.duration = duration
    
    def execute(self, context):

        try:
            template = cv2.imread(self.reference_path, cv2.IMREAD_COLOR)
            
            if template is None:
                print(f"Image not found: {self.reference_path}")
                return None
            
            # Convertir template a escala de grises ANTES de usarlo
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template_height, template_width = template_gray.shape
            
            screenshot = pyautogui.screenshot()
            screenshot_width, screenshot_height = screenshot.size

            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            screenshot_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            threshold = 0.8

            if max_val >= threshold:

                top_left = max_loc
                center_x = top_left[0] + template_width // 2
                center_y = top_left[1] + template_height // 2

                x_ratio = center_x / screenshot_width
                y_ratio = center_y / screenshot_height

                x = round(x_ratio * screenshot_width)
                y = round(y_ratio * screenshot_height)

                pyautogui.moveTo(x, y, duration=self.duration)
                pyautogui.click(button=self.type, clicks=self.clicks, interval=self.delay)

                log_action(context, f"Reference found. Clicked at coordinates: ({x}, {y})", "👆")

            else:
                print(f"No coincidence found (confidence: {max_val:.4f}, threshold: {threshold})")
            
        except Exception as e:
            print(f"Error: {e}")
            log_action(context, f"Error: {e}", "❌")