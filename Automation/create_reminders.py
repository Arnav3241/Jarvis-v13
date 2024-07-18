# Import necessary modules
import os.path  # Module for working with file paths
from google.auth.transport.requests import Request  # Module for handling authentication requests
from google.oauth2.credentials import Credentials  # Module for managing OAuth2.0 credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # Module for handling OAuth 2.0 authentication flow
from googleapiclient.discovery import build  # Module for building API service objects

# Define the access scope for the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Function to get Google Calendar API credentials
def get_credentials():
    creds = None
    # Check if the file 'CREDENTIALS\token.json' exists
    if os.path.exists(r"Automation//API//token.json"):
        # Load credentials from the file if it exists
        creds = Credentials.from_authorized_user_file(r"Automation//API//token.json")
        
    
    # Check if credentials do not exist or are invalid
    if not creds or not creds.valid:
        # Check if credentials exist, are expired, and can be refreshed
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            creds.refresh(Request())
            
        else:
            # Create a flow for handling OAuth 2.0 authentication
            flow = InstalledAppFlow.from_client_secrets_file(r"Automation//API//credentials.json", SCOPES)
            # Run the OAuth 2.0 authentication flow locally
            creds = flow.run_local_server(port=0)
            
        
        # Save the refreshed or newly obtained credentials to 'CREDENTIALS\token.json'
        with open(r"Automation//API//token.json", "w") as token:
            token.write(creds.to_json())
            
        
    
    # Return the obtained credentials
    return creds


# Function to create a Google Calendar event with reminders
def create_event_with_reminders(service):
    try:
        # Define the details of the event with reminders
        event = {"summary": "Meeting with Reminders", "location": "Conference Room", "start": {"dateTime": "2024-07-17T10:00:00+05:30", "timeZone": "Asia/Kolkata"}, "end": {"dateTime": "2024-07-17T11:00:00+05:30", "timeZone": "Asia/Kolkata"}, "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 30}, {"method": "email", "minutes": 60}]}}
        
        # Insert the event into the Google Calendar and execute the request
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        # Print the link to view the created event
        print(f"Event created: {created_event.get('htmlLink')}")
        
    
    # Handle exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
        
    

# Main function
def main():
    # Get Google Calendar API credentials
    creds = get_credentials()
    # Build the Google Calendar API service object
    service = build("calendar", "v3", credentials=creds)
    
    # Create an event with reminders
    create_event_with_reminders(service)
    

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
    