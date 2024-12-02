from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from utils import decrypt
import json, os
from dotenv import load_dotenv


def gdrive():
    load_dotenv('.env')
    key = os.getenv('KEY')
    if not key:
        raise ValueError("KEY not found in environment variables")

    key = key.encode()
    secret = decrypt(key)
    try:
        secret = json.loads(secret)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse decrypted secret as JSON")

    scope = ['https://www.googleapis.com/auth/drive']
    Excel_SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    scopes = scope + Excel_SCOPE

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(secret, scopes)

    gauth = GoogleAuth()
    gauth.credentials = credentials

    print("Successfully authenticated with Google Drive API")
    GoogleDrive(gauth).ListFile()
    return GoogleDrive(gauth)


def find_or_create_folder(service, folder_id, target_folder_name):
    """Find the folder with the specified name among the subfolders. If it doesn't exist, create it."""
    # Query to list subfolders of the specified folder
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    items = service.ListFile({'q': query}).GetList()
    print(f"{folder_id = }")

    # Search for the folder by name
    for item in items:
        if item['title'] == target_folder_name:
            print(f"Folder '{target_folder_name}' found with ID: {item['id']}")
            return item['id']

    # If the folder doesn't exist, create it
    print(f"No folder named '{target_folder_name}' found. Creating it.")
    folder_metadata = {
        'title': target_folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': folder_id}]
    }
    folder = service.CreateFile(folder_metadata)
    folder.Upload()
    print(f"Folder '{target_folder_name}' created with ID: {folder['id']}")
    return folder['id']


if _name_ == "_main_":
    pass
