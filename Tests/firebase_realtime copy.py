import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyautogui import hotkey
import time
import requests
import os

def download_image(image_url, filename="downloaded_image.jpg"):
    print("Trying to download image...")
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Image downloaded successfully!")
    else:
        print(
            f"Failed to download the image. Status code: {response.status_code}")

    return filename


def Image_Firebase_Link(db_url='https://jarvis-5b1c9-default-rtdb.asia-southeast1.firebasedatabase.app/', cred_json_filepath=r'Mobile/jarvis-5b1c9-firebase-adminsdk-w4ny1-5cf73bb898.json'):
    cred = credentials.Certificate(cred_json_filepath)
    firebase_admin.initialize_app(cred, {
        'databaseURL': db_url
    })

    ref = db.reference('/Link')
    
    print("Waiting for the image link to be uploaded...")

    while True:
        current_value = ref.get()
        if current_value != '':
            print(f'Current value in the database: {current_value}')
            ref.set('')
            file_save_loc = download_image(current_value, filename=f"{os.getcwd()}//Download//{time.time()}.jpg")
            os.startfile(file_save_loc)
            

        time.sleep(2)


if __name__ == '__main__':
    Image_Firebase_Link()
