import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def getCredentials():
  creds = None
  
  if os.path.exists("Automation//API//token.json"):
    print("Loading credentials from file")
    creds = Credentials.from_authorized_user_file(f"Automation//API//token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          f"{os.getcwd()}//Automation//API//credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open(f"Automation//APItoken.json", "w") as token:
      token.write(creds.to_json())
  return creds

def CreateEvent(service):
  try:
    event = {
      "summary": "Test Event",
      "location": "Test Location",
      "description": "Test Description",
      "colorId": 6,
      "start": {
        "dateTime": "2024-07-17T09:00:00+05:30",
        "timeZone": "Asia/Kolkata",
      },
      "end": {
        "dateTime": "2024-07-17T17:00:00+05:30",
        "timeZone": "Asia/Kolkata",
      },
      "recurrence": [
        "RRULE:FREQ=DAILY;COUNT=1"
      ],
      "attendees": [  
        {"email": "arnav.singh.legendary.202@gmail.com"},
        {"email": "jarvis.ai.v12@gmail.com"}
      ],
    }
    
    created_data = service.events().insert(calendarId="primary", body=event).execute()
    print("Event created: %s" % (created_data.get("htmlLink")))
  except HttpError as error:
    print("An error occurred: %s" % error)
    
def main():
  creds = getCredentials()
  service = build("calendar", "v3", credentials=creds)
  CreateEvent(service)
  
if __name__ == "__main__":
  main()