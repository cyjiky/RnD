import os
import httplib2 
from googleapiclient.discovery import build 
from oauth2client.service_account import ServiceAccountCredentials

# pip install httplib2 google-api-python-client google-auth-httplib2 google-auth
# pip install oauth2client

class SheetService:
    @staticmethod 
    def get_service_sheets():
        base_dir = os.path.dirname(os.path.abspath(__file__))

        creds_json = os.path.join(base_dir, 'creds', 'sheets_API_key.json')

        scopes = ['https://www.googleapis.com/auth/spreadsheets']

        if not os.path.exists(creds_json):
            raise FileExistsError(f"File not found: {creds_json}")
        
        creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
        return build('sheets', 'v4', http=creds_service)
    
    
    def __init__(self):
        self.service = self.get_service_sheets()

        if not self.service:
            raise Exception("Failed to initialize Google Sheets service")
        self.spreadsheets = self.service.spreadsheets()


    def values(self):
        return self.spreadsheets.values()
