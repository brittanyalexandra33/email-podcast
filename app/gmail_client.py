import base64
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pathlib

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def _token_paths(secrets_dir: str):
    sd = pathlib.Path(secrets_dir)
    sd.mkdir(parents=True, exist_ok=True)
    return sd / 'gmail_token.json', sd / 'client_secret.json'

def gmail_service(secrets_dir: str):
    token_path, client_secret_path = _token_paths(secrets_dir)
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def list_messages(service, q: str, max_n: int = 30) -> List[str]:
    resp = service.users().messages().list(userId='me', q=q, maxResults=max_n).execute()
    return [m['id'] for m in resp.get('messages', [])]

def get_message(service, mid: str) -> Dict:
    return service.users().messages().get(userId='me', id=mid, format='full').execute()

def get_header(msg: Dict, name: str) -> Optional[str]:
    for h in msg.get('payload', {}).get('headers', []):
        if h['name'].lower() == name.lower():
            return h['value']
    return None

def get_html_body(msg: Dict) -> str:
    def walk(part):
        if part.get('mimeType') == 'text/html' and 'data' in part.get('body', {}):
            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
        for p in part.get('parts', []) or []:
            html = walk(p)
            if html: return html
        return None
    return walk(msg.get('payload', {})) or ""
