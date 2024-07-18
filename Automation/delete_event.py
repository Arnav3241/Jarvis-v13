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
    
    creds = None
    # Check if the file '"Automation//API//token.json' exists
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


# Function to delete a Google Calendar event
def delete_event(service, calendar_id, event_id):
    try:
        # Execute the request to delete the specified event
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        # Print a success message
        print(f"Event with ID '{event_id}' deleted successfully.")
        
    
    # Handle HTTP errors
    except HttpError as error:
        # Check if the error is due to the event not found
        if error.resp.status == 404:
            print(f"Error: Event with ID '{event_id}' not found.")
            
        # Check if the error is due to insufficient permissions
        elif error.resp.status == 403:
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
    
    # Assuming you have the event_id of the event to delete
    event_id_to_delete = "cooelrg6qrcpvk947d7o4i4gv0"
    
    # Delete the event
    delete_event(service, "primary", event_id_to_delete)
    

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
    