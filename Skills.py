"""
Made by Arnav Singh (https://github.com/Arnav3241) & Avi Sinha (https://github.com/Avi0981) with 💖
"""

import random
from dotenv import load_dotenv
from typing import Tuple, Optional
import base64
from datetime import datetime
from Functions.Speak import Speak
from winotify import Notification, audio
from datetime import datetime, timedelta
from Functions.Listen import Listen
import google.generativeai as genai
from bs4 import BeautifulSoup
import urllib.parse
import webbrowser
import pyperclip
import speedtest
import wikipedia
import pywhatkit
import threading
import requests
import keyboard
import platform
import sqlite3
import shutil
import ctypes
import psutil
import socket
import time
import json
import nltk
import os
import requests
from bs4 import BeautifulSoup
from icrawler.builtin import GoogleImageCrawler

arduino_port = 'COM3'
baud_rate = 9600

try:
    from nltk.corpus import wordnet
except:
    nltk.download('wordnet')

with open('api_keys.json', 'r') as f:
    ld = json.loads(f.read())
    api = ld["gemini1"]
    news_api = ld["newsapi"]

genai.configure(api_key=api)


def googleSearch(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
    except Exception:
        Speak("Error occurred in function 'googleSearch' (in file Skills.py)")


def getWeather(location):
    try:
        search_url = f"https://www.google.com/search?q=weather+{location.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        temperature = soup.find("span", attrs={"id": "wob_tm"}).text
        description = soup.find("span", attrs={"id": "wob_dc"}).text
        if location != "":
            weather_info = f"The current temperature in {location} is {temperature}°C with {description}."
        else:
            weather_info = f"The current temperature is {temperature}°C with {description}."

        return weather_info
    except Exception:
        Speak("Error occurred in function 'getWeather' (in file Skills.py)")


def sendWhatsApp(contact_number, message):
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=f"+91{contact_number}", message=message, tab_close=True)
    except Exception:
        Speak("Error occurred in function 'sendWhatsApp' (in file Skills.py)")


def playMusic(song_name):
    try:
        import pywhatkit
        pywhatkit.playonyt(song_name)
    except Exception:
        Speak("Error occurred in function 'playMusic' (in file Skills.py)")


def getTodayDate():
    try:
        return datetime.now().strftime("%Y-%m-%d")
    except Exception:
        Speak("Error occurred in function 'getTodayDate' (in file Skills.py)")


def getSystemInfo(info_type):
    try:
        if info_type == "CPU":
            return f"{psutil.cpu_percent(interval=1)}%"
        elif info_type == "RAM":
            ram = psutil.virtual_memory()
            return f"{ram.percent}%"
        elif info_type == "DISK":
            disk = psutil.disk_usage('/')
            return f"{disk.percent}%"
        elif info_type == "BATTERY":
            battery = psutil.sensors_battery()
            return f"{battery.percent}%" if battery else "Not available"
        else:
            return "Invalid info type"
    except Exception:
        Speak("Error occurred in function 'getSystemInfo' (in file Skills.py)")


def getCurrentTime():
    try:
        return datetime.now().strftime("%H:%M:%S")
    except Exception:
        Speak("Error occurred in function 'getCurrentTime' (in file Skills.py)")


def getCurrentDay():
    try:
        return datetime.now().strftime("%A")
    except Exception:
        Speak("Error occurred in function 'getCurrentDay' (in file Skills.py)")


def getSelectedData():
    try:
        keyboard.press_and_release("ctrl+c")
        time.sleep(0.5)
        return str(pyperclip.paste())
    except Exception:
        Speak("Error occurred in function 'getSelectedData' (in file Skills.py)")


def getClipboardData():
    try:
        return str(pyperclip.paste())
    except Exception:
        Speak("Error occurred in function 'getClipboardData' (in file Skills.py)")


def copyToClipboard(text):
    try:
        pyperclip.copy(text)
    except Exception:
        Speak("Error occurred in function 'copyToClipboard' (in file Skills.py)")


def Sleep():
    try:
        if platform.system() == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif platform.system() == "Linux":
            os.system("systemctl suspend")
        elif platform.system() == "Darwin":  # macOS
            os.system("pmset sleepnow")
    except Exception:
        Speak("Error occurred in function 'Sleep' (in file Skills.py)")


def Shutdown():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /s /t 0")
        elif platform.system() == "Linux":
            os.system("shutdown now")
        elif platform.system() == "Darwin":  # macOS
            os.system("sudo shutdown -h now")
    except Exception:
        Speak("Error occurred in function 'Shutdown' (in file Skills.py)")


def Restart():
    try:
        if platform.system() == "Windows":
            os.system("shutdown /r /t 0")
        elif platform.system() == "Linux":
            os.system("reboot")
        elif platform.system() == "Darwin":  # macOS
            os.system("sudo shutdown -r now")
    except Exception:
        Speak("Error occurred in function 'Restart' (in file Skills.py)")


def Lock():
    try:
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif platform.system() == "Linux":
            os.system("gnome-screensaver-command -l")
        elif platform.system() == "Darwin":  # macOS
            os.system("pmset displaysleepnow")
    except Exception:
        Speak("Error occurred in function 'Lock' (in file Skills.py)")


def newMeeting():
    try:
        webbrowser.open("https://meet.new")
    except Exception:
        Speak("Error occurred in function 'newMeeting' (in file Skills.py)")


def wordRelations(word, relation_type):
    try:
        synsets = wordnet.synsets(word)
        if relation_type == "meaning":
            if synsets:
                meanings = [synset.definition() for synset in synsets]
                return ', '.join(meanings) if meanings else "No meaning found"
            else:
                return "No meaning found"
        elif relation_type == "synonym":
            if synsets:
                synonyms = set()
                for synset in synsets:
                    synonyms.update(lemma.name() for lemma in synset.lemmas())
                return ', '.join(synonyms) if synonyms else "No synonyms found"
            else:
                return "No synonyms found"
        elif relation_type == "antonym":
            if synsets:
                antonyms = set()
                for synset in synsets:
                    for lemma in synset.lemmas():
                        antonyms.update(antonym.name()
                                        for antonym in lemma.antonyms())
                return ', '.join(antonyms) if antonyms else "No antonyms found"
            else:
                return "No antonyms found"
        else:
            return "Invalid relation type"
    except Exception:
        Speak("Error occurred in function 'wordRelations' (in file Skills.py)")


def writeViaKeyboard(text):
    try:
        keyboard.write(text)
    except Exception:
        Speak("Error occurred in function 'writeViaKeyboard' (in file Skills.py)")


def voiceTyping():
    try:
        a = Listen()
        writeViaKeyboard(a)
    except Exception:
        Speak("Error occurred in function 'voiceTyping' (in file Skills.py)")


def websiteScanner():
    try:
        chrome_history_path = os.path.expanduser(
            '~') + r"\AppData\Local\Google\Chrome\User Data\Profile 1\History"
        history_db_path = os.path.join(os.getcwd(), "ChromeHistoryCopy.txt")
        shutil.copy2(chrome_history_path, history_db_path)
        conn = sqlite3.connect(history_db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 1")
        latest_url = cursor.fetchone()[0]
        conn.close()
        os.remove(history_db_path)

        print("Latest URL:", latest_url)

        jinna_url = "https://r.jina.ai"
        query = f"{jinna_url}/{latest_url}"
        response = requests.get(query)
        print(response.text)

        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        responseAI = model.generate_content(f"""
            {response.text}

            QUERY : Given is a textual representation of the website.
            Summarize this with all the key points mentioned
        """)

        return responseAI.text
    except Exception:
        Speak("Error occurred in function 'websiteScanner' (in file Skills.py)")


def checkInternetSpeed():
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        return int(download_speed), int(upload_speed)
    except Exception:
        Speak("Error occurred in function 'checkInternetSpeed' (in file Skills.py)")


def getPublicIP():
    try:
        ip = requests.get("https://api.ipify.org").text
        return ip
    except Exception:
        Speak("Error occurred in function 'getPublicIP' (in file Skills.py)")


def getLocalIP():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception:
        Speak("Error occurred in function 'getLocalIP' (in file Skills.py)")


def searchWikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        Speak("Error occurred in function 'searchWikipedia' (in file Skills.py)")


def getCryptoPrice(crypto="bitcoin"):
    try:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd'
        response = requests.get(url)
        data = response.json()
        return data[crypto]['usd']
    except Exception:
        Speak("Error occurred in function 'getCryptoPrice' (in file Skills.py)")


def searchAndOpen(product_name):
    try:
        product_name = urllib.parse.quote_plus(product_name)

        webbrowser.open(f"https://www.amazon.com/s?k={product_name}")
        webbrowser.open(f"https://www.ebay.com/sch/i.html?_nkw={product_name}")
        webbrowser.open(f"https://www.flipkart.com/search?q={product_name}")
    except Exception:
        Speak("Error occurred in function 'searchAndOpen' (in file Skills.py)")


def textSummarisation(text):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        responseAI = model.generate_content(f"""
            {text}

            QUERY : Given above is a piece of text.
            Summarize this text in a few words without omitting any key points of the text.
        """)

        return responseAI.text
    except Exception:
        Speak("Error occurred in function 'textSummarisation' (in file Skills.py)")


def getNews():
    try:
        news_str = ""
        urls = []

        url = (f'https://newsapi.org/v2/everything?'
               f'q=india&'
               f'from={(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")}&'
               f'to={datetime.today()}&'
               f'sortBy=popularity&'
               f'language=en&'
               f'apiKey={news_api}'
               )

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, Message: {response.text}")
        else:
            data = response.json()
            if 'articles' in data and data['articles']:
                a = 10
                b = 0
                for article in data['articles']:
                    news_str += f"{article['title']}: {article['description']}\n\n"
                    urls.append(article['url'])
                    b = b + 1
                    if b == a:
                        break
            else:
                news_str = "No articles found."

        return news_str, urls
    except Exception:
        Speak("Error occurred in function 'getNews' (in file Skills.py)")


def toastNotification(app_id, title, msg, duration, icon, loop):
    try:
        toast = Notification(app_id=app_id, title=title,
                             msg=msg, duration=duration, icon=icon)

        if loop:
            toast.set_audio(audio.LoopingCall, loop=True)
        else:
            toast.set_audio(audio.Default, loop=False)

        toast.show()
    except Exception:
        Speak("Error occurred in function 'toastNotification' (in file Skills.py)")


################### NOT TO BE USED BY GEMINI #######################

def IM_getCurrentTime():
    try:
        current_time = datetime.now()
        hour = current_time.strftime("%I").lstrip(
            '0')  # Remove leading zero from hour
        minute = current_time.strftime("%M")
        formatted_time = f"{hour}:{minute}"
        return formatted_time
    except Exception:
        Speak("Error occurred in function 'IM_getCurrentTime' (in file Skills.py)")


def UpdateTasks():
    try:
        global tasks
        with open('todolist.txt', 'r') as f:
            todolist = f.read()
        tasks = todolist.split('\n')
    except Exception:
        Speak("Error occurred in function 'UpdateTasks' (in file Skills.py)")

################### TO-DO LIST FUNCTIONS ###########################


TDL_ACTIVE = True
tasks = []


def TDL_activate():
    try:
        global TDL_ACTIVE
        TDL_ACTIVE = True

        def daemonTask():
            while TDL_ACTIVE:
                UpdateTasks()

                to_delete = []
                for task in tasks:
                    if task.split(' ')[0] == IM_getCurrentTime():
                        toastNotification("Jarvis Todo", "Task time!", task.split(
                            ' ')[1], "long", f"{os.getcwd()}/Assets/Images/Jarvis.png", True)
                        to_delete.append(task)

                for task in to_delete:
                    tasks.remove(task)

                if len(to_delete) != 0:
                    with open('todolist.txt', 'w') as f:
                        for i in range(len(tasks)):
                            if i != len(tasks) - 1:
                                f.write(f'{tasks[i]}\n')
                                continue
                            f.write(f'{tasks[i]}')

        threading.Thread(target=daemonTask, daemon=True).start()
    except Exception:
        Speak("Error occurred in function 'TDL_activate' (in file Skills.py)")


def TDL_deactivate():
    try:
        global TDL_ACTIVE
        TDL_ACTIVE = False
    except Exception:
        Speak("Error occurred in function 'TDL_deactivate' (in file Skills.py)")


def TDL_add(hours, minutes, task_name):
    try:
        with open('todolist.txt', 'a') as f:
            f.write(f'\n{hours}:{minutes} {task_name}')
    except Exception:
        Speak("Error occurred in function 'TDL_add' (in file Skills.py)")


def TDL_show():
    try:
        os.system(f"notepad.exe {os.getcwd()}/todolist.txt")
    except Exception:
        Speak("Error occurred in function 'TDL_show' (in file Skills.py)")

###################################################################


def scrape_google(query, count):
    try:
        google_Crawler = GoogleImageCrawler(
            storage={'root_dir': f'{os.getcwd()}\\Download\\{query}'})
        google_Crawler.crawl(keyword=query, max_num=count)
        files = []
        for i in range(count):
            files.append(f'{os.getcwd()}\\Download\\{query}\\{str(i+1).zfill(6)}')
        return files
    except Exception:
        Speak("Error occured in function 'scrape_google' (in file Skills.py)")


def generate_AI(prompt: str, seed: int = 1800647681, width: int = 1024, height: int = 576, steps: int = 4, enhance: bool = True, safety_filter: bool = True, image_path: str = "Downloads/image.jpg") -> Tuple[bool, Optional[str]]:
    """
    Generates an image based on the given parameters and saves it to a file.

    Parameters:
    - prompt (str): Description of the image to generate.
    - seed (int): Seed for the image generation process.
    - width (int): Width of the generated image.
    - height (int): Height of the generated image.
    - steps (int): Number of steps for the image generation process. More the Steps More Clear and Realistic Image 
    - enhance (bool): Whether to enhance the image quality.
    - safety_filter (bool): Whether to apply a safety filter to the image.

    - For Square Image Size: 768x768
    - For Portrait Image Size: 1024x576
    - For Landscape Image Size: 576x1024

    Returns:
    - Tuple[bool, Optional[str]]: A tuple containing a boolean indicating the success of the API call,
      and an optional string with the file path where the image is saved if successful.
    """

    # Define the URL and headers for the API call
    url = "https://turbo.decohere.ai/generate/turbo"
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcklkIjoiY3VzX1FkMkZqUmhwekVUYnc3IiwiaWF0IjoxNzIzMTg0Nzg2LCJleHAiOjE3MjMxODU2ODZ9.fPEpOFzGTskjEhNTmH1fRwQ3Rh7g5694NEjLlBJbVI64GifPTWR7O-2cciaxhiIZjYFnRa8xsKwvr7m8kERM_N8WFqX7U3Bas-4ROnV_PKrbT7Eb88tidmWfaXOaBocjtLiMlcPFDKh2Qxy0J-FKDRWZQhPJknkD-e_v9PW7maBbxDGsIq6DRulBqk8qjZ-yskcfyqKuX3HupKXbaOCQOPwWqsNlvNRYbgGIjQP2sb03exhF5ixWUUDhFCfCfoCgYKlFJTXlc9dYViC0ewnLINMsCcWpJxPCiW1cy5dB4Lh0AvNOi_xLIkcMzEtegO-cXmfYGvIl7d4A6juxaNRDyA",
    }

    # Define the payload for the POST request
    payload = {
        "prompt": prompt,
        "seed": seed,
        "width": width,
        "height": height,
        "steps": steps,
        "enhance": enhance,
        "safety_filter": safety_filter,
    }

    # Make the POST request to the API
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 200:
        # Extract base64 encoded image data
        base64_image_data = response.json().get('image', '')
        # Decode base64 encoded image data to bytes
        image_bytes = base64.b64decode(base64_image_data)
        # Write the bytes to a file as an image
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)
        return True, image_path
    else:
        print(f"API call failed with status code {response.status_code}")
        return False, response.text


if __name__ == "__main__":
    try:
        # t = time.time()
        # generate_AI('Cake', seed=random.randint(1, 100000),
        #             image_path=f"{os.getcwd()}//Download/image{random.randint(1, 100000)}.jpg")
        # print(time.time() - t)
        print(scrape_google('Monkeys', 10))
    except Exception as e:
        print(e)
        # Speak("Error occurred in the main block (in file Skills.py)")
