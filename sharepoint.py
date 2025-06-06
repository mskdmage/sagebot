from dotenv import load_dotenv
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os

load_dotenv()

sage_email = os.getenv("SAGE_EMAIL")
sage_password = os.getenv("SAGE_PASSWORD")
sage_sharepoint_url = os.getenv("SAGE_SHAREPOINT_URL")
sage_sharepoint_folder = os.getenv("SAGE_SHAREPOINT_FOLDER")

folder_relative_url = f"/sites/{sage_sharepoint_folder}/Shared Documents"

ctx = ClientContext(sage_sharepoint_url).with_credentials(UserCredential(sage_email, sage_password))

folder = ctx.web.get_folder_by_server_relative_url(folder_relative_url)
ctx.load(folder)
ctx.load(folder.files)
ctx.load(folder.folders)
ctx.execute_query()