from dotenv import load_dotenv
from automate import *

load_dotenv()

sage_email = os.getenv("SAGE_EMAIL")
sage_password = os.getenv("SAGE_PASSWORD")
sage_sharepoint_url = os.getenv("SAGE_SHAREPOINT_URL")








print_banner()

bot = SageBot(
    OpenPage("https://www.google.com"),
    Wait(1),
    ClickElement('xpath=//*[@id="APjFqb"]'),
    FillInput('xpath=//*[@id="APjFqb"]', "Hello, world!"),
    SubmitForm('xpath=//*[@id="APjFqb"]'),
    Sleep(5),
    Screenshot(),
    Wait(1),
    OpenPage("https://www.duckduckgo.com"),
    Wait(1),    
    ClickOnReference("1"),
    Sleep(5),
    Screenshot(),
)

bot.execute()