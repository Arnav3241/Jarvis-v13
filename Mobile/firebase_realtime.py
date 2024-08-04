from firebase_admin import credentials, storage, db
from urllib.parse import unquote
import firebase_admin
import requests
import time
import json
import os

# Load configuration details from JSON file securely
try:
    with open(os.path.join(os.getcwd(), 'api_keys.json'), 'r') as f:
        ld = json.load(f)
        DB_URL = ld.get("DB_URL", "")
        Cred_JSON_Filepath = ld.get("Cred_JSON_Filepath", "")
        storageBucket = ld.get("storage_bucket", "")
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading configuration: {e}")
    exit(1)  # Exit if configuration can't be loaded

# Initialize Firebase app with credentials and database URL
def initialize_firebase(cred_json_filepath, db_url, storage_bucket):
    cred = credentials.Certificate(cred_json_filepath)
    firebase_admin.initialize_app(cred, {
        'storageBucket': storage_bucket,
        'databaseURL': db_url
    })

# Download image from URL and save it locally
def download_image(image_url, filename="downloaded_image.jpg"):
    print("Trying to download image...")
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Image downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image. Error: {e}")
    return filename

# Delete a specific image from Firebase Storage
def delete_image_from_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    try:
        blob.delete()
        print(f"Deleted image from Firebase Storage at: {file_path}")
    except Exception as e:
        print(f"Failed to delete image from Firebase Storage at: {file_path}. Error: {e}")

# Delete all images under the 'images/' directory in Firebase Storage
def delete_all_images_from_directory(directory):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=directory)
    for blob in blobs:
        try:
            blob.delete()
            print(f"Deleted image from Firebase Storage at: {blob.name}")
        except Exception as e:
            print(f"Failed to delete image from Firebase Storage at: {blob.name}. Error: {e}")

# Main function to link Firebase and handle image operations
def Image_Firebase_Link(db_url=DB_URL, cred_json_filepath=Cred_JSON_Filepath):
    storage_bucket = storageBucket
    initialize_firebase(cred_json_filepath, db_url, storage_bucket)

    ref = db.reference('/Link')
    print("Waiting for the image link to be uploaded...")

    while True:
        current_value = ref.get()
        if current_value:
            print(f'Current value in the database: {current_value}')
            ref.set('')  # Reset the database reference

            file_save_loc = download_image(current_value, filename=f"{os.getcwd()}/Download/{time.time()}.jpg")
            try:
                # Extract and decode the path from the URL
                path_start = current_value.find('/o/') + len('/o/')
                path_end = current_value.find('?')
                firebase_file_path = current_value[path_start:path_end]
                firebase_file_path = unquote(firebase_file_path)
                # delete_image_from_firebase(firebase_file_path)
                delete_all_images_from_directory('images/')
            except IndexError:
                print("Failed to extract the correct file path from the URL.")

        time.sleep(2)

# Function to be called for deleting all images
def delete_all_images():
    Image_Firebase_Link()  # Ensure Firebase is initialized

if __name__ == '__main__':
    delete_all_images()
