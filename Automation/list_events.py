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

# Function to list events in a Google Calendar
def list_events(service, calendar_id="primary"):
    try:
        # Execute the request to list events in the specified calendar
        events_result = service.events().list(calendarId=calendar_id).execute()
        events = events_result.get("items", [])
        
        # Check if no events were found
        if not events:
            print("No events found.")
            
        else:
            # Print details of each event found
            print("Events:")
            for event in events:
                print(f"{event['summary']} - {event['id']}")
                
            
        
    # Handle exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
        
    

# Main function
def main():
    # Get Google Calendar API credentials
    creds = get_credentials()
    # Build the Google Calendar API service object
    service = build("calendar", "v3", credentials=creds)
    
    # List events in the default calendar
    list_events(service)
    

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
    