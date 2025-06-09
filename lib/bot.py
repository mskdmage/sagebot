"""Core SageBot automation classes and context management."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page


class SageBot:
    """Main automation bot class that orchestrates the execution of automation steps.
    
    This class manages the lifecycle of browser automation, coordinating between
    different automation steps and maintaining the execution context.
    """
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the SageBot with automation functions and configuration.
        
        Args:
            *args: Variable length argument list of automation functions to execute.
            **kwargs: Arbitrary keyword arguments for bot configuration.
                headless (bool): Whether to run browser in headless mode. Defaults to False.
                state_name (str): Name of the state to load. Defaults to None.
        """
        self.context: BotContext = BotContext()
        self.functions: List[Any] = [f for f in args]
        self.headless: bool = kwargs.get("headless", False)
        self.state_name: Optional[str] = kwargs.get("state_name", None)
        BotContext.log_action(self.context, "Booting up SageBot", "🤖")

    def execute(self) -> None:
        """Execute all automation functions in sequence.
        
        This method starts the browser, loads state if specified, and executes
        all registered automation functions in order. It handles cleanup and
        error reporting.
        """
        BotContext.log_action(self.context, "SageBot execution started.", "🤖")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=self.headless, args=["--start-maximized"])
        
        if self.state_name:
            context = browser.new_context(storage_state=f"./states/{self.state_name}.json")
            BotContext.log_action(self.context, f"Loaded state {self.state_name}", "💾")
        else:
            context = browser.new_context()
            BotContext.log_action(self.context, "No state name provided, creating new context", "💾")

        self.context.set_playwright(playwright)
        self.context.set_browser(browser)
        self.context.set_context(context)

        for function in self.functions:
            try:
                self.context = function.execute(self.context)
            except Exception as e:
                BotContext.log_action(self.context, f"Error executing {function.__class__.__name__}: {e}", "❌")
                break
            
        self.context.browser.close()
        self.context.playwright.stop()
        BotContext.log_action(self.context, "Bot execution completed", "🏁")


class BotContext:
    """Context manager for bot execution state and browser resources.
    
    This class maintains the state of the automation session, including
    browser instances, pages, data storage, and logging functionality.
    """
    
    def __init__(self) -> None:
        """Initialize the bot context with default values."""
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.current_element: Optional[Any] = None
        self.data: Dict[str, Any] = {}
        self.pages: List[Page] = []
        self.run_name: str = BotContext.generate_timestamp()
        self.run_folder: str = f"./runs/{self.run_name}"
        BotContext.create_run_folder(self.run_folder)
    
    def set_playwright(self, playwright: Playwright) -> 'BotContext':
        """Set the Playwright instance.
        
        Args:
            playwright: The Playwright instance to use.
            
        Returns:
            Self for method chaining.
        """
        self.playwright = playwright
        return self

    def set_browser(self, browser: Browser) -> 'BotContext':
        """Set the browser instance.
        
        Args:
            browser: The browser instance to use.
            
        Returns:
            Self for method chaining.
        """
        self.browser = browser
        return self
    
    def set_context(self, context: BrowserContext) -> 'BotContext':
        """Set the browser context.
        
        Args:
            context: The browser context to use.
            
        Returns:
            Self for method chaining.
        """
        self.context = context
        return self
    
    def set_page(self, page: Page) -> 'BotContext':
        """Set the current page and add it to the pages list.
        
        Args:
            page: The page instance to set as current.
            
        Returns:
            Self for method chaining.
        """
        self.page = page
        if page not in self.pages:
            self.pages.append(page)
        return self
    
    def set_current_element(self, element: Any) -> 'BotContext':
        """Set the currently selected element.
        
        Args:
            element: The element to set as current.
            
        Returns:
            Self for method chaining.
        """
        self.current_element = element
        return self

    def get_page(self, index: int = -1) -> Optional[Page]:
        """Get a page by index from the pages list.
        
        Args:
            index: Index of the page to retrieve. Defaults to -1 (last page).
            
        Returns:
            The page at the specified index, or current page if no pages in list.
        """
        return self.pages[index] if self.pages else self.page
    
    def store_data(self, key: str, value: Any) -> 'BotContext':
        """Store data in the context.
        
        Args:
            key: The key to store the data under.
            value: The value to store.
            
        Returns:
            Self for method chaining.
        """
        self.data[key] = value
        return self
    
    def get_run_folder(self) -> str:
        """Get the run folder path.
        
        Returns:
            The path to the current run folder.
        """
        return self.run_folder
    
    def get_data(self, key: str) -> Any:
        """Retrieve stored data by key.
        
        Args:
            key: The key to retrieve data for.
            
        Returns:
            The stored value or None if key doesn't exist.
        """
        return self.data.get(key)
      
    @staticmethod
    def log_action(context: 'BotContext', action: str, outcome: str = "👌") -> None:
        """Log an action to console and file.
        
        Args:
            context: The bot context instance.
            action: Description of the action performed.
            outcome: Emoji or symbol representing the outcome. Defaults to "👌".
        """
        data = f"[{outcome}] {BotContext.get_current_datetime()} - {action}"
        print(data)
        with open(f"{context.get_run_folder()}/actions.log", "a", encoding="utf-8") as f:
            f.write(data + "\n")

    @staticmethod
    def generate_timestamp() -> str:
        """Generate a timestamp string for file naming.
        
        Returns:
            Timestamp string in YYYYMMDDHHMMSS format.
        """
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    @staticmethod
    def get_current_datetime() -> str:
        """Get current datetime in readable format.
        
        Returns:
            Current datetime string in YYYY-MM-DD HH:MM:SS format.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def create_run_folder(run_folder: str) -> None:
        """Create the run folder for logging and artifacts.
        
        Args:
            run_folder: Path to the run folder to create.
        """
        os.makedirs(run_folder, exist_ok=True)