"""GUI automation classes for desktop interaction using PyAutoGUI and OpenCV."""

import cv2
import numpy as np
from PIL import Image
import pyautogui
from datetime import datetime
from time import sleep
from random import randint
import os
from typing import Union, List, Tuple, Any

from .bot import BotContext


class GUIStep:
    """Base class for all GUI automation steps."""
    
    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        """Get the screen size.
        
        Returns:
            Tuple containing screen width and height in pixels.
        """
        return pyautogui.size()


class Click(GUIStep):
    """Perform a mouse click at the current cursor position."""
    
    def __init__(self, type: str = "left", clicks: int = 1, delay: int = 100, wait: int = 0) -> None:
        """Initialize click step.
        
        Args:
            type: Type of click ('left', 'right', 'middle'). Defaults to "left".
            clicks: Number of clicks to perform. Defaults to 1.
            delay: Delay between clicks in milliseconds. Defaults to 100.
            wait: Time to wait after clicking in milliseconds. Defaults to 0.
        """
        self.type = type
        self.clicks = clicks
        self.delay = delay / 1000
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the click step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        pyautogui.click(button=self.type, clicks=self.clicks, interval=self.delay)
        BotContext.log_action(context, f"Clicked {self.type} {self.clicks} times with {self.delay*1000}ms delay", "👆")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        return context


class MouseMove(GUIStep):
    """Move the mouse cursor to a position based on screen ratio."""
    
    def __init__(self, x_ratio: float, y_ratio: float, duration: int = 500, wait: int = 0) -> None:
        """Initialize mouse move step.
        
        Args:
            x_ratio: X position as a ratio of screen width (0.0 to 1.0).
            y_ratio: Y position as a ratio of screen height (0.0 to 1.0).
            duration: Duration of the movement in milliseconds. Defaults to 500.
            wait: Time to wait after moving in milliseconds. Defaults to 0.
        """
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.duration = duration / 1000
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the mouse move step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        w, h = GUIStep.get_screen_size()
        x = round(self.x_ratio * w)
        y = round(self.y_ratio * h)
        pyautogui.moveTo(x, y, duration=self.duration)
        BotContext.log_action(context, f"Moved mouse to {x}, {y} with {self.duration*1000}ms duration", "👆")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        return context


class DragTo(GUIStep):
    """Drag the mouse to a position based on screen ratio."""
    
    def __init__(self, x_ratio: float, y_ratio: float, duration: int = 500, wait: int = 0) -> None:
        """Initialize drag step.
        
        Args:
            x_ratio: X position as a ratio of screen width (0.0 to 1.0).
            y_ratio: Y position as a ratio of screen height (0.0 to 1.0).
            duration: Duration of the drag in milliseconds. Defaults to 500.
            wait: Time to wait after dragging in milliseconds. Defaults to 0.
        """
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.duration = duration / 1000
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the drag step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        w, h = GUIStep.get_screen_size()
        x = round(self.x_ratio * w)
        y = round(self.y_ratio * h)
        pyautogui.dragTo(x, y, duration=self.duration)
        BotContext.log_action(context, f"Dragged to {x}, {y} with {self.duration*1000}ms duration", "👆")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        return context


class Screenshot(GUIStep):
    """Take a screenshot and save it to the run folder."""
    
    def __init__(self, delay: int = 1000, wait: int = 0) -> None:
        """Initialize screenshot step.
        
        Args:
            delay: Delay before taking screenshot in milliseconds. Defaults to 1000.
            wait: Time to wait after taking screenshot in milliseconds. Defaults to 0.
        """
        self.delay = delay / 1000
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the screenshot step.
        
        Args:
            context: The bot context for logging and file paths.
            
        Returns:
            The bot context (unchanged).
        """
        sleep(self.delay)
        filename = f"{BotContext.generate_timestamp()}.png"
        pyautogui.screenshot(f"{context.get_run_folder()}/{filename}")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        BotContext.log_action(context, f"Took screenshot {filename}", "📷")
        return context


class Keys(GUIStep):
    """Press keyboard keys or key combinations."""
    
    def __init__(self, key_sequences: Union[str, List[str], Tuple[str, ...]], wait: int = 0) -> None:
        """Initialize key press step.
        
        Args:
            key_sequences: Key sequences to press. Can be a string, list, or tuple.
            wait: Time to wait after pressing keys in milliseconds. Defaults to 0.
        """
        self.key_sequences = key_sequences if isinstance(key_sequences, list) else [key_sequences]
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the key press step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        for sequence in self.key_sequences:
            if isinstance(sequence, tuple):
                for key in sequence:
                    pyautogui.keyDown(key)
                for key in reversed(sequence):
                    pyautogui.keyUp(key)
            else:
                pyautogui.press(sequence)
        BotContext.log_action(context, f"Pressed {self.key_sequences}", "🔄")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        return context


class TypeKeys(GUIStep):
    """Type text using the keyboard."""
    
    def __init__(self, keys: str, wait: int = 0) -> None:
        """Initialize type keys step.
        
        Args:
            keys: Text to type.
            wait: Time to wait after typing in milliseconds. Defaults to 0.
        """
        self.keys = keys
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the type keys step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        pyautogui.typewrite(self.keys)
        BotContext.log_action(context, f"Typed {self.keys}", "📝")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        return context


class Sleep(GUIStep):
    """Sleep for a specified duration with optional randomization."""
    
    def __init__(self, duration: int = 3000, randomize: bool = True, wait: int = 0) -> None:
        """Initialize sleep step.
        
        Args:
            duration: Base sleep duration in milliseconds. Defaults to 3000.
            randomize: Whether to randomize the duration slightly. Defaults to True.
            wait: Additional wait time after sleep in milliseconds. Defaults to 0.
        """
        self.duration = duration / 1000
        self.randomize = randomize
        self.wait = wait / 1000

    def execute(self, context: BotContext) -> BotContext:
        """Execute the sleep step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        actual_duration = self.duration
        if self.randomize:
            min_duration = max(int(self.duration - 1), 1)
            max_duration = max(int(self.duration + 1), min_duration)
            actual_duration = randint(min_duration, max_duration) / 1000 if min_duration != max_duration else self.duration
        
        sleep(actual_duration)
        BotContext.log_action(context, f"Slept for {actual_duration*1000:.0f}ms", "⏳")
        if self.wait > 0:
            sleep(self.wait)
            BotContext.log_action(context, f"Waited {self.wait*1000}ms", "⏳")
        return context


class ClickAt(GUIStep):
    """Click at specific absolute coordinates."""
    
    def __init__(self, x: int, y: int, type: str = "left", clicks: int = 1, delay: int = 100, wait: int = 0) -> None:
        """Initialize click at coordinates step.
        
        Args:
            x: X coordinate in pixels.
            y: Y coordinate in pixels.
            type: Type of click ('left', 'right', 'middle'). Defaults to "left".
            clicks: Number of clicks to perform. Defaults to 1.
            delay: Delay between clicks in milliseconds. Defaults to 100.
            wait: Time to wait after clicking in milliseconds. Defaults to 0.
        """
        self.x = x
        self.y = y
        self.type = type
        self.clicks = clicks
        self.delay = delay / 1000
        self.wait = wait / 1000
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the click at coordinates step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        BotContext.log_action(context, f"🎯 Clicking at absolute coordinates: ({self.x}, {self.y})", "🎯")
        
        pyautogui.moveTo(self.x, self.y, duration=0.5)
        pyautogui.click(button=self.type, clicks=self.clicks, interval=self.delay)
        
        BotContext.log_action(context, f"✅ Successfully clicked at ({self.x}, {self.y})", "👆")
        
        if self.wait > 0:
            BotContext.log_action(context, f"⏳ Starting wait of {self.wait*1000:.0f}ms after click", "⏳")
            sleep(self.wait)
            BotContext.log_action(context, f"✅ Completed wait of {self.wait*1000:.0f}ms", "⏳")
        
        return context


class ClickOnReference(GUIStep):
    """Click on a reference image found on the screen using template matching."""
    
    def __init__(self, reference_file: str, type: str = "left", clicks: int = 1, delay: int = 100, 
                 duration: int = 100, wait: int = 0, threshold: float = 0.8) -> None:
        """Initialize click on reference image step.
        
        Args:
            reference_file: Name of the reference image file (without .png extension).
            type: Type of click ('left', 'right', 'middle'). Defaults to "left".
            clicks: Number of clicks to perform. Defaults to 1.
            delay: Delay between clicks in milliseconds. Defaults to 100.
            duration: Duration of mouse movement in milliseconds. Defaults to 100.
            wait: Time to wait after clicking in milliseconds. Defaults to 0.
            threshold: Confidence threshold for template matching (0.0 to 1.0). Defaults to 0.8.
        """
        self.reference_path = f"./references/{reference_file}.png"
        self.type = type
        self.clicks = clicks
        self.delay = delay / 1000
        self.duration = duration / 1000
        self.wait = wait / 1000
        self.threshold = threshold
        
    def execute(self, context: BotContext) -> BotContext:
        """Execute the click on reference image step.
        
        Args:
            context: The bot context for logging.
            
        Returns:
            The bot context (unchanged).
        """
        BotContext.log_action(context, f"🔍 Searching for reference image: {self.reference_path}", "🔍")
        
        try:
            template = cv2.imread(self.reference_path, cv2.IMREAD_COLOR)
            
            if template is None:
                error_msg = f"Image not found: {self.reference_path}"
                print(error_msg)
                BotContext.log_action(context, error_msg, "❌")
                if self.wait > 0:
                    sleep(self.wait)
                    BotContext.log_action(context, f"Waited {self.wait*1000:.0f}ms after error", "⏳")
                return context
            
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template_height, template_width = template_gray.shape
            
            BotContext.log_action(context, f"📏 Template size: {template_width}x{template_height}", "📏")
            
            screenshot = pyautogui.screenshot()
            screenshot_width, screenshot_height = screenshot.size

            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            screenshot_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)

            result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            BotContext.log_action(context, f"🎯 Match confidence: {max_val:.4f} (threshold: {self.threshold})", "🎯")

            if max_val >= self.threshold:
                top_left = max_loc
                center_x = top_left[0] + template_width // 2
                center_y = top_left[1] + template_height // 2

                x_ratio = center_x / screenshot_width
                y_ratio = center_y / screenshot_height

                x = round(x_ratio * screenshot_width)
                y = round(y_ratio * screenshot_height)

                BotContext.log_action(context, f"🎯 Reference found! Moving to coordinates: ({x}, {y})", "🎯")
                
                pyautogui.moveTo(x, y, duration=self.duration)
                pyautogui.click(button=self.type, clicks=self.clicks, interval=self.delay)
                
                BotContext.log_action(context, f"✅ Successfully clicked at coordinates: ({x}, {y})", "👆")
                
                if self.wait > 0:
                    BotContext.log_action(context, f"⏳ Starting wait of {self.wait*1000:.0f}ms after successful click", "⏳")
                    sleep(self.wait)
                    BotContext.log_action(context, f"✅ Completed wait of {self.wait*1000:.0f}ms", "⏳")

                return context

            else:
                error_msg = f"❌ No reference match found (confidence: {max_val:.4f}, needed: {self.threshold})"
                print(error_msg)
                BotContext.log_action(context, error_msg, "❌")
            
        except Exception as e:
            error_msg = f"❌ Error in ClickOnReference: {e}"
            print(error_msg)
            BotContext.log_action(context, error_msg, "❌")
        
        BotContext.log_action(context, "❌ ClickOnReference failed - executing fallback wait", "❌")
        if self.wait > 0:
            BotContext.log_action(context, f"⏳ Starting fallback wait of {self.wait*1000:.0f}ms", "⏳")
            sleep(self.wait)
            BotContext.log_action(context, f"✅ Completed fallback wait of {self.wait*1000:.0f}ms", "⏳")
        return context