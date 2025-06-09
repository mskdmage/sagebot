"""Browser automation classes for web interaction using Playwright."""

import os
from typing import Optional, Any
from playwright.sync_api import Page, Locator

from .bot import BotContext
from .gui import GUIStep


class BrowserStep:
    """Base class for all browser automation steps."""
    
    @staticmethod
    def parse_selector(x_path: Optional[str], css: Optional[str]) -> str:
        """Parse and format selector for Playwright.
        
        Args:
            x_path: XPath selector string.
            css: CSS selector string.
            
        Returns:
            Properly formatted selector string for Playwright.
            
        Raises:
            ValueError: If no selector is provided.
        """
        if x_path:
            return "xpath=" + x_path
        elif css:
            return "css=" + css
        else:
            raise ValueError("No selector provided")


class NewPage(BrowserStep):
    """Create a new browser page and optionally navigate to a URL."""
    
    def __init__(self, url: Optional[str] = None, wait: int = 0) -> None:
        """Initialize a new page creation step.
        
        Args:
            url: URL to navigate to after creating the page. Defaults to None.
            wait: Time to wait in milliseconds after navigation. Defaults to 0.
        """
        self.url = url
        self.wait = wait
        self.width, self.height = GUIStep.get_screen_size()
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the new page creation step.
        
        Args:
            context: The bot context containing browser instances.
            
        Returns:
            Updated bot context with the new page set.
        """
        page = context.context.new_page()
        page.set_viewport_size({"width": self.width, "height": self.height})

        try:
            page.evaluate("() => { if (window.screen) { window.moveTo(0, 0); window.resizeTo(screen.width, screen.height); } }")
            BotContext.log_action(context, f"Maximized browser window to {self.width}x{self.height}", "🖥️")
        except:
            page.set_viewport_size({"width": self.width, "height": self.height})
            BotContext.log_action(context, f"Set viewport size to {self.width}x{self.height}", "🖥️")
        
        BotContext.log_action(context, f"Opened new browser page.", "🌐")
        if self.url:
            page.goto(self.url)
            BotContext.log_action(context, f"Navigated to {self.url}", "🌐")
        if self.wait > 0:
            page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        return context.set_page(page)


class GoToURL(BrowserStep):
    """Navigate to a specific URL."""
    
    def __init__(self, url: str, wait: int = 0) -> None:
        """Initialize URL navigation step.
        
        Args:
            url: URL to navigate to.
            wait: Time to wait in milliseconds after navigation. Defaults to 0.
        """
        self.url = url
        self.wait = wait
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the URL navigation step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            The bot context (unchanged).
        """
        context.page.goto(self.url)
        BotContext.log_action(context, f"Navigated to {self.url}", "🌐")
        if self.wait > 0:
            context.page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        return context


class Wait(BrowserStep):
    """Wait for a specified duration."""
    
    def __init__(self, miliseconds: int) -> None:
        """Initialize wait step.
        
        Args:
            miliseconds: Time to wait in milliseconds.
        """
        self.miliseconds = miliseconds
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the wait step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            The bot context (unchanged).
        """
        context.page.wait_for_timeout(self.miliseconds)
        BotContext.log_action(context, f"Waited {self.miliseconds}ms", "⏳")
        return context


class ClickElement(BrowserStep):
    """Click on an element identified by selector."""
    
    def __init__(self, x_path: Optional[str] = None, css: Optional[str] = None, wait: int = 0) -> None:
        """Initialize element click step.
        
        Args:
            x_path: XPath selector for the element. Defaults to None.
            css: CSS selector for the element. Defaults to None.
            wait: Time to wait in milliseconds after clicking. Defaults to 0.
        """
        self.selector = BrowserStep.parse_selector(x_path, css)
        self.wait = wait
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the element click step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            Updated bot context with the clicked element set as current.
        """
        element = context.page.locator(self.selector)
        if element:
            context.set_current_element(element)
            context.current_element.click()
            BotContext.log_action(context, f"Clicked element {self.selector}", "👆")
        else:
            BotContext.log_action(context, f"Element {self.selector} not found", "❌")
        if self.wait > 0:
            context.page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        return context


class FillInput(BrowserStep):
    """Fill an input field with a value."""
    
    def __init__(self, x_path: Optional[str] = None, css: Optional[str] = None, value: Optional[str] = None, wait: int = 0) -> None:
        """Initialize input fill step.
        
        Args:
            x_path: XPath selector for the input element. Defaults to None.
            css: CSS selector for the input element. Defaults to None.
            value: Value to fill in the input. Defaults to None.
            wait: Time to wait in milliseconds after filling. Defaults to 0.
        """
        self.selector = BrowserStep.parse_selector(x_path, css)
        self.value = value
        self.wait = wait
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the input fill step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            The bot context (unchanged).
        """
        context.page.fill(self.selector, self.value)
        BotContext.log_action(context, f"Filled input {self.selector} with {self.value}", "📝")
        if self.wait > 0:
            context.page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        return context


class FillAndSubmit(BrowserStep):
    """Fill an input field and submit by pressing Enter."""
    
    def __init__(self, x_path: Optional[str] = None, css: Optional[str] = None, value: Optional[str] = None, wait: int = 0) -> None:
        """Initialize fill and submit step.
        
        Args:
            x_path: XPath selector for the input element. Defaults to None.
            css: CSS selector for the input element. Defaults to None.
            value: Value to fill in the input. Defaults to None.
            wait: Time to wait in milliseconds after submitting. Defaults to 0.
        """
        self.selector = BrowserStep.parse_selector(x_path, css)
        self.value = value
        self.wait = wait
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the fill and submit step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            The bot context (unchanged).
        """
        context.page.fill(self.selector, self.value)
        context.page.press(self.selector, "Enter")
        if self.wait > 0:
            context.page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        BotContext.log_action(context, f"Filled and submitted {self.selector} with {self.value}", "📝")
        return context


class ClickAndDownload(BrowserStep):
    """Click an element and handle file download."""
    
    def __init__(self, x_path: Optional[str] = None, css: Optional[str] = None, wait: int = 0, 
                 download_path: str = "downloads", download_name: Optional[str] = None) -> None:
        """Initialize click and download step.
        
        Args:
            x_path: XPath selector for the element. Defaults to None.
            css: CSS selector for the element. Defaults to None.
            wait: Time to wait in milliseconds after downloading. Defaults to 0.
            download_path: Directory path to save downloads. Defaults to "downloads".
            download_name: Custom name for downloaded file. Defaults to None.
        """
        self.selector = BrowserStep.parse_selector(x_path, css)
        self.download_path = download_path
        self.download_name = download_name
        self.wait = wait
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the click and download step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            Updated bot context with the clicked element set as current.
        """
        element = context.page.locator(self.selector)
        if element:
            context.set_current_element(element)
            with context.page.expect_download() as download_info:
                context.current_element.click()
                download = download_info.value
                BotContext.log_action(context, f"Download started: {download.url}", "💾")
                
                if self.download_name is None:
                    suggested_filename = download.suggested_filename
                    if suggested_filename:
                        _, extension = os.path.splitext(suggested_filename)
                        final_name = f"{BotContext.generate_timestamp()}{extension}"
                    else:
                        url_path = download.url.split('/')[-1]
                        if '.' in url_path and not url_path.endswith('/'):
                            _, extension = os.path.splitext(url_path.split('?')[0])
                            final_name = f"{BotContext.generate_timestamp()}{extension}"
                        else:
                            final_name = BotContext.generate_timestamp()
                else:
                    final_name = self.download_name
                
                os.makedirs(self.download_path, exist_ok=True)
                download.save_as(f"{self.download_path}/{final_name}")
                BotContext.log_action(context, f"Download completed: {final_name}", "💾")

            BotContext.log_action(context, f"Clicked element {self.selector}", "👆")
        else:
            BotContext.log_action(context, f"Element {self.selector} not found", "❌")
        if self.wait > 0:
            context.page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        return context


class HandleDialog(BrowserStep):
    """Handle browser dialogs (alerts, confirms, prompts)."""
    
    @staticmethod
    def accept(dialog: Any) -> None:
        """Accept a dialog.
        
        Args:
            dialog: The dialog object to accept.
        """
        dialog.accept()
    
    @staticmethod
    def dismiss(dialog: Any) -> None:
        """Dismiss a dialog.
        
        Args:
            dialog: The dialog object to dismiss.
        """
        dialog.dismiss()

    def __init__(self, accept: bool = True, wait: int = 0) -> None:
        """Initialize dialog handler step.
        
        Args:
            accept: Whether to accept dialogs. If False, dialogs are dismissed. Defaults to True.
            wait: Time to wait in milliseconds after setting up handler. Defaults to 0.
        """
        self.accept = accept
        self.wait = wait
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the dialog handler setup step.
        
        Args:
            context: The bot context containing the current page.
            
        Returns:
            The bot context (unchanged).
        """
        if self.accept:
            context.page.on("dialog", self.accept)
            BotContext.log_action(context, "Set up dialog handler to accept dialogs", "✅")
        else:
            context.page.on("dialog", self.dismiss)
            BotContext.log_action(context, "Set up dialog handler to dismiss dialogs", "❌")
            
        if self.wait > 0:
            context.page.wait_for_timeout(self.wait)
            BotContext.log_action(context, f"Waited {self.wait}ms", "⏳")
        return context


class StoreState(BrowserStep):
    """Store the current browser state to a file."""
    
    def __init__(self, state_name: str) -> None:
        """Initialize state storage step.
        
        Args:
            state_name: Name of the state file (without extension).
        """
        self.state_name = state_name
    
    def execute(self, context: BotContext) -> BotContext:
        """Execute the state storage step.
        
        Args:
            context: The bot context containing the browser context.
            
        Returns:
            The bot context (unchanged).
        """
        path = f"./states"
        os.makedirs(path, exist_ok=True)
        context.context.storage_state(path=f"{path}/{self.state_name}.json")
        BotContext.log_action(context, f"Stored state {self.state_name}", "💾")
        return context

