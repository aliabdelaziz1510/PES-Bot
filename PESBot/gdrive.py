from utils import decrypt
from dotenv import load_dotenv


from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json
import os

def gdrive():
    load_dotenv('.env')
    key = os.getenv('KEY')
    if not key:
        raise ValueError("KEY not found in environment variables")

    key = key.encode()
    secret = decrypt(key)  # Ensure decrypt returns a valid JSON string
    try:
        secret = json.loads(secret)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse decrypted secret as JSON")

    scopes = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets.readonly',
    ]

    # Use google.oauth2.credentials instead of PyDrive's GoogleAuth
    credentials = Credentials.from_service_account_info(secret, scopes=scopes)

    # Build and return the Google Drive API service
    service = build('drive', 'v3', credentials=credentials)
    print("Successfully authenticated with Google Drive API")
    return service



def find_or_create_folder(service, parent_folder_id, target_folder_name):
    """
    Find the folder with the specified name among the subfolders.
    If it doesn't exist, create it.
    """
    # Query to list subfolders of the specified folder
    query = f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()

    # Search for the folder by name
    items = response.get('files', [])
    for item in items:
        if item['name'] == target_folder_name:
            print(f"Folder '{target_folder_name}' found with ID: {item['id']}")
            return item['id']

    # If the folder doesn't exist, create it
    print(f"No folder named '{target_folder_name}' found. Creating it.")
    folder_metadata = {
        'name': target_folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    print(f"Folder '{target_folder_name}' created with ID: {folder['id']}")
    return folder['id']


if __name__ == "__main__":
    pass
