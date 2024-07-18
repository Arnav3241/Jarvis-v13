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

# Function to get details of a specific event
def get_event_details(service, calendar_id, event_id):
    try:
        # Get the details of the specified event
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        # Print the details of the event
        print(f"\nEvent Details : {event['summary']} (Event ID: {event['id']}):")
        print(f"Start Time: {event['start']['dateTime']}")
        print(f"End Time: {event['end']['dateTime']}")
        print(f"Location: {event.get('location', 'N/A')}")
        print(f"Description: {event.get('description', 'N/A')}")
        print(f"Attendees: {', '.join(attendee['email'] for attendee in event.get('attendees', []))}")
        print(f"Reminders: {event.get('reminders', {})}")
        
    
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        
    

# Function to search for events with a specific query
def search_events(service, query):
    try:
        # Execute a search for events with a specific query
        events_result = service.events().list(calendarId="primary", timeMin="2023-11-01T00:00:00Z", timeMax="2023-11-30T23:59:59Z", q=query).execute()
        
        # Get the list of matching events
        events = events_result.get("items", [])
        
        # Check if no events were found
        if not events:
            print("No events found.")
            
        else:
            # Print details of each matching event
            print("Matching Events:")
            for event in events:
                # Call the function to get and print details of the event
                get_event_details(service, "primary", event['id'])
                
            
        
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        
    
# Main function
def main():
    # Get Google Calendar API credentials
    creds = get_credentials()
    # Build the Google Calendar API service object
    service = build("calendar", "v3", credentials=creds)
    
    # Search for events with a specific query
    search_query = "jarvis"
    search_events(service, search_query)
    

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
    