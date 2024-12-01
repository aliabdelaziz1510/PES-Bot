from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def gsheet():
  # Set up Google Drive API authentication using a service account
  scope = ['https://www.googleapis.com/auth/drive']
  Excel_SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
  scopes = scope + Excel_SCOPE
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      "RAScloud.json", scopes)
  return build('sheets', 'v4', credentials=credentials)


if __name__ == '__main__':
  gsheet()
