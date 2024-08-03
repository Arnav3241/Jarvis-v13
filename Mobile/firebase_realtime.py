from firebase_admin import credentials, storage, db
from urllib.parse import unquote
import firebase_admin
import requests
import time
import json
import os


with open(f'{os.getcwd()}//api_keys.json', 'r') as f:
  ld = json.loads(f.read())
  DB_URL = ld["DB_URL"]
  Cred_JSON_Filepath = ld["Cred_JSON_Filepath"]
  storageBucket = ld["storage_bucket"]
  

def initialize_firebase(cred_json_filepath, db_url, storage_bucket):
    cred = credentials.Certificate(cred_json_filepath)
    firebase_admin.initialize_app(cred, {
        'storageBucket': storage_bucket,
        'databaseURL': db_url
    })

def download_image(image_url, filename="downloaded_image.jpg"):
    print("Trying to download image...")
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Image downloaded successfully!")
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

    return filename

def delete_image_from_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    try:
        blob.delete()
        print(f"Deleted image from Firebase Storage at: {file_path}")
    except Exception as e:
        print(f"Failed to delete image from Firebase Storage at: {file_path}. Error: {e}")

def Image_Firebase_Link(db_url=DB_URL, cred_json_filepath=Cred_JSON_Filepath):
    storage_bucket = storageBucket
    initialize_firebase(cred_json_filepath, db_url, storage_bucket)

    ref = db.reference('/Link')

    print("Waiting for the image link to be uploaded...")

    while True:
        current_value = ref.get()
        if current_value != '':
            print(f'Current value in the database: {current_value}')
            ref.set('')  # Reset the database reference

            # Assume the current_value is a URL containing the path in Firebase Storage
            file_save_loc = download_image(current_value, filename=f"{os.getcwd()}/Download/{time.time()}.jpg")
            os.startfile(file_save_loc)

            # Extract the path from the current_value URL
            try:
                firebase_file_path = current_value.split('/o/')[1].split('?')[0]
                firebase_file_path = unquote(firebase_file_path)
                delete_image_from_firebase(firebase_file_path)
            except IndexError:
                print("Failed to extract the correct file path from the URL.")

        time.sleep(2)

if __name__ == '__main__':
    Image_Firebase_Link()
