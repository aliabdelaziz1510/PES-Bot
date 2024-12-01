from gsheet import gsheet
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
from _log import _logger


def logTask(name, id, task_number, project_number, file_name):

  Mechanical_users = [
      'eslamsala7',
      'ibrahimeid.',
      'osamaasharaf',
      'mohameddawoud._37071',
      'mahmoud_ramdan',
      'abdallah.galal.',
      'mohammedwaly.162',
      'mohamed_fathy.',
      'youssefsalama0532',
  ]
  Log_SPREADSHEET_ID = '1v2O_JudvfyR120nCS1RcVpDrN8FcnNDclwoOsSfyYPI'

  if str(id) in Mechanical_users:
    Log_RANGE_NAME = 'Mechanical Members!A1:Z100'
  else:
    Log_RANGE_NAME = 'Electrical Members!A1:Z100'

  try:
    service = gsheet()
    # time
    now_date = datetime.now().date()
    now_time = (datetime.now() + timedelta(hours=2)).strftime('%H:%M:%S')

    data = [[
        name, id, task_number, project_number, file_name,
        str(now_date),
        str(now_time)
    ]]

    # Call the Sheets API
    sheet = service.spreadsheets()
    add = sheet.values().append(spreadsheetId=Log_SPREADSHEET_ID,
                                range=Log_RANGE_NAME,
                                body={
                                    "majorDimension": "ROWS",
                                    "values": data
                                },
                                valueInputOption="USER_ENTERED").execute()
  except HttpError as err:
    _logger().error(err)


if __name__ == "__main__":
  logTask()
