"""Main application entry point for SageBot automation."""

from lib import (
    SageBot,
    browser,
    gui,
    files
)


def main() -> None:
    """Execute the main SageBot automation workflow.
    
    This function creates a SageBot instance with a series of browser automation
    steps and executes them in sequence.
    """
    bot = SageBot(
        browser.NewPage("https://www.weiloja.edu.ec"),
        browser.ClickElement(x_path='//*[@id="menu-principal-menu-1"]/li[2]/a', wait=2000),
        browser.ClickElement(x_path='//*[@id="wa"]/div[1]/div[2]', wait=2000),
        browser.ClickElement(x_path='//*[@id="wa"]/div[2]/div[2]/div[2]/div[1]/a', wait=2000),
        browser.HandleDialog(accept=False, wait=2000),
        browser.GoToURL("https://www.weiloja.edu.ec/wp-content/", wait=2000),
        gui.Screenshot(delay=1000, wait=2000),
        browser.StoreState("state_test"),
        state_name="state_test",
        headless=True,
    )
    
    bot.execute()


if __name__ == "__main__":
    main()