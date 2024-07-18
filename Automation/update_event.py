# Import necessary modules
import os.path  # Module for working with file paths
from google.auth.transport.requests import Request  # Module for handling authentication requests
from google.oauth2.credentials import Credentials  # Module for managing OAuth2.0 credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # Module for handling OAuth 2.0 authentication flow
from googleapiclient.discovery import build  # Module for building API service objects
from googleapiclient.errors import HttpError  # Module for handling Google API errors

# Define the access scope for the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Function to get Google Calendar API credentials
def get_credentials():
    
    creds = None # Initialize credentials as None
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
            
        
    return creds # Return the obtained credentials

# Function to update a Google Calendar event
def update_event(service, calendar_id, event_id, updated_event):
    try:
        # Execute the request to update the specified event
        updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_event).execute()
        
        # Print the link to view the updated event
        print(f"Event updated: {updated_event.get('htmlLink')}")
        
    
    # Handle HTTP errors
    except HttpError as error:
        # Check if the error is due to insufficient permissions
        if error.resp.status == 403:
            print("Error: Insufficient permissions. Make sure your application has the correct scopes.")
            
        else:
            # Print other errors
            print(f"An error occurred: {error}")
            
        
    
# Main function
def main():
    # Get Google Calendar API credentials
    creds = get_credentials()
    # Build the Google Calendar API service object
    service = build("calendar", "v3", credentials=creds)
    
    # Assuming you have the event_id of the event to update
    event_id_to_update = "05n6ghva399jm7elthrt1nqkig"
    
    # Fetch the existing event details
    existing_event = service.events().get(calendarId="primary", eventId=event_id_to_update).execute()
    
    # Update the event details
    updated_event = {"summary": "Updated Event Summary", "location": "Updated Location", "description": "Updated Description", 'start': {'dateTime': '2023-11-20T10:00:00+05:30', 'timeZone': 'Asia/Kolkata'}, 'end': {'dateTime': '2023-11-20T18:00:00+05:30', 'timeZone': 'Asia/Kolkata'}, "recurrence": ["RRULE:FREQ=DAILY;COUNT=3"], 'attendees': [{'email': 'updated@example.com'}]}
    
    # Update the event
    update_event(service, "primary", event_id_to_update, updated_event)

# Run the main function if this script is executed
if __name__ == "__main__":
        main()
        