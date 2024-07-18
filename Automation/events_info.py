import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

        
def get_credentials():
    creds = None
    if os.path.exists(r"Automation//API//token.json"):
        creds = Credentials.from_authorized_user_file(r"Automation//API//token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r"Automation//API//credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open(r"Automation//API//token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def list_events(calendar_id="primary"):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    try:
        events_result = service.events().list(calendarId=calendar_id).execute()
        events = events_result.get("items", [])

        if not events:
            print("No events found.")
        else:
            print("Events:")
            for event in events:
                print(f"{event['summary']} - {event['id']}")
                print(f"Start Time: {event['start']['dateTime']}")
                print(f"End Time: {event['end']['dateTime']}")
                print(f"Location: {event.get('location', 'N/A')}")
                print(f"Description: {event.get('description', 'N/A')}")
                print(f"Attendees: {', '.join(attendee['email'] for attendee in event.get('attendees', []))}")
                print(f"Reminders: {event.get('reminders', {})}")
                print("\n")
                

    except Exception as e:
        print(f"An error occurred: {e}")

list_events()