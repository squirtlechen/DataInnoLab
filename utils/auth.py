import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class OAuthService:
    def __init__(self):
        self.credentials_file = 'innolab_login_client_secret.json'
        self.token_file = 'user_token.json'
        self.scopes =  [
           'https://www.googleapis.com/auth/spreadsheets.readonly',
           'https://www.googleapis.com/auth/gmail.compose',
           'https://www.googleapis.com/auth/userinfo.email',
           'openid'
           ]
        self.creds = None
        self.user_email = None

    def authenticate(self):
        """Authenticate and return the credentials."""
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        if not self.creds or not self.creds.valid:
          if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            print("Token refreshed.")
            self.save_token()
          else:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
            self.creds = flow.run_local_server(port=0)
            print("Authenticated via browser.")
            self.save_token()
        self.print_user_info()
        return self.creds

    def save_token(self):
        """Save the credentials token to a file."""
        with open(self.token_file, 'w') as token:
            token.write(self.creds.to_json())

    def print_user_info(self):
        """Print the authenticated user's info."""
        service = build('oauth2', 'v2', credentials=self.creds)
        user_info = service.userinfo().get().execute()
        self.user_email = user_info['email']
        print(f"Authenticated user: {self.user_email}")
        
    def get_service(self, service_name, version):
        """Build and return a Google API service."""
        if not self.creds:
            self.authenticate()
        return build(service_name, version, credentials=self.creds)