from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def generate_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_run_folder(run_folder):
    os.makedirs(run_folder, exist_ok=True)

def log_action(context, action, outcome="👌"):
    data = f"[{outcome}] {get_current_datetime()} - {action}"
    print(data)
    with open(f"{context.get_run_folder()}/actions.log", "a", encoding="utf-8") as f:
        f.write(data + "\n")

class BotContext:
    def __init__(self):
        self.browser = None
        self.page = None
        self.current_element = None
        self.data = {}
        self.pages = []
        self.run_name = generate_timestamp()
        self.run_folder = f"./runs/{self.run_name}"
        create_run_folder(self.run_folder)
    
    def set_browser(self, browser):
        self.browser = browser
        return self
    
    def set_page(self, page):
        self.page = page
        if page not in self.pages:
            self.pages.append(page)
        return self
    
    def get_page(self, index=-1):
        return self.pages[index] if self.pages else self.page
    
    def store_data(self, key, value):
        self.data[key] = value
        return self
    
    def get_run_folder(self):
        return self.run_folder

class SageBot:
    def __init__(self, *args, **kwargs):
        self.functions = [f for f in args]
        self.context = BotContext()
        log_action(self.context, "Starting bot", "🤖")

    def execute(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False, slow_mo=1000)
            self.context.set_browser(browser)
            
            for function in self.functions:
                if isinstance(function, PlaywrightStep):
                    self.context = function.execute(self.context)
                else:
                    function.execute(self.context)
            
            log_action(self.context, "Bot execution completed", "🏁")
            browser.close()

class PlaywrightStep:
    pass

class OpenPage(PlaywrightStep):
    def __init__(self, url):
        self.url = url
    
    def execute(self, context):
        page = context.browser.new_page()
        page.goto(self.url)
        log_action(context, f"Opened page {self.url}", "🌐")
        return context.set_page(page)

class Wait(PlaywrightStep):
    def __init__(self, seconds):
        self.miliseconds = seconds * 1000
    
    def execute(self, context):
        context.page.wait_for_timeout(self.miliseconds)
        log_action(context, f"Waited {self.miliseconds / 1000} miliseconds", "⏳")
        return context

class ClickElement(PlaywrightStep):
    def __init__(self, selector):
        self.selector = selector
    
    def execute(self, context):
        element = context.page.locator(self.selector)
        element.click()
        context.current_element = element
        log_action(context, f"Clicked element {self.selector}", "👆")
        return context

class FillInput(PlaywrightStep):
    def __init__(self, selector, value):
        self.selector = selector
        self.value = value
    
    def execute(self, context):
        context.page.fill(self.selector, self.value)
        log_action(context, f"Filled input {self.selector} with {self.value}", "📝")
        return context

class ExtractText(PlaywrightStep):
    def __init__(self, selector, store_as=None):
        self.selector = selector
        self.store_as = store_as
    
    def execute(self, context):
        text = context.page.locator(self.selector).text_content()
        if self.store_as:
            context.store_data(self.store_as, text)
        log_action(context, f"Extracted text from {self.selector}", "📄")
        return context

class GoToPage(PlaywrightStep):
    def __init__(self, page_index):
        self.page_index = page_index
    
    def execute(self, context):
        target_page = context.get_page(self.page_index)
        context.page = target_page
        log_action(context, f"Switched to page {self.page_index}", "🔄")
        return context

class ConditionalAction(PlaywrightStep):
    def __init__(self, condition_func, action):
        self.condition_func = condition_func
        self.action = action
    
    def execute(self, context):
        if self.condition_func(context):
            log_action(context, f"Condition met, executed {self.action}", "🔄")
            return self.action.execute(context)
        log_action(context, f"Condition not met, skipping {self.action}", "❌")
        return context

class WaitForSelector(PlaywrightStep):
    def __init__(self, selector, timeout=10000):
        self.selector = selector
        self.timeout = timeout
    
    def execute(self, context):
        context.page.wait_for_selector(self.selector, timeout=self.timeout)
        log_action(context, f"Waited for selector {self.selector}", "⏳")
        return context

class FillAndSubmit(PlaywrightStep):
    def __init__(self, selector, value):
        self.selector = selector
        self.value = value
    
    def execute(self, context):
        context.page.fill(self.selector, self.value)
        context.page.press(self.selector, "Enter")
        log_action(context, f"Filled and submitted {self.selector} with {self.value}", "📝")
        return context

class SubmitForm(PlaywrightStep):
    def __init__(self, selector="form"):
        self.selector = selector
    
    def execute(self, context):
        try:
            submit_btn = context.page.locator(f'{self.selector} input[type="submit"], {self.selector} button[type="submit"]').first
            submit_btn.click()
            log_action(context, f"Submitted form {self.selector}", "📝")
        except:
            context.page.press(self.selector, "Enter")
            log_action(context, f"Submitted form {self.selector} with Enter", "📝")
        return context