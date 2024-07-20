from Functions.SpeakSync import SpeakSync as Speak
from Functions.Listen import Listen
import google.generativeai as genai
from datetime import datetime
from bs4 import BeautifulSoup
import webbrowser
import pyperclip
import pywhatkit
import requests
import keyboard
import platform
import sqlite3
import shutil
import ctypes
import psutil
import random
import time
import json
import nltk
import os

try: from nltk.corpus import wordnet
except: nltk.download('wordnet')


with open('api_keys.json', 'r') as f:
  api = json.loads(f.read())["gemini1"]

genai.configure(api_key=api)

def googleSearch(query):
  search_url = f"https://www.google.com/search?q={query}"
  webbrowser.open(search_url)
  
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
  except:
    return "Couldn't find the weather for that location."

def sendWhatsApp(contact_number, message):
  try: pywhatkit.sendwhatmsg_instantly(phone_no=f"+91{contact_number}", message=message, tab_close=True)
  except: Speak("Couldn't send the message.")

def playMusic(song_name):
  import pywhatkit
  pywhatkit.playonyt(song_name)

def getTodayDate():
  return datetime.now().strftime("%Y-%m-%d")

def getSystemInfo(info_type):
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

def generateRandomNumber(lower_limit, upper_limit):
  return str(random.randint(lower_limit, upper_limit))

def getCurrentTime():
  return datetime.now().strftime("%H:%M:%S")

def getCurrentDay():
  return datetime.now().strftime("%A")

def getSelectedData():
  keyboard.press_and_release("ctrl+c")
  time.sleep(0.5) 
  return str(pyperclip.paste())

def getClipboardData():
  return str(pyperclip.paste())

def copyToClipboard(text):
  pyperclip.copy(text)

def Sleep():
  if platform.system() == "Windows":
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
  elif platform.system() == "Linux":
    os.system("systemctl suspend")
  elif platform.system() == "Darwin":  # macOS
    os.system("pmset sleepnow")

def Shutdown():
  if platform.system() == "Windows":
    os.system("shutdown /s /t 0")
  elif platform.system() == "Linux":
    os.system("shutdown now")
  elif platform.system() == "Darwin":  # macOS
    os.system("sudo shutdown -h now")

def Restart():
  if platform.system() == "Windows":
    os.system("shutdown /r /t 0")
  elif platform.system() == "Linux":
    os.system("reboot")
  elif platform.system() == "Darwin":  # macOS
    os.system("sudo shutdown -r now")

def Lock():
  if platform.system() == "Windows":
    ctypes.windll.user32.LockWorkStation()
  elif platform.system() == "Linux":
    os.system("gnome-screensaver-command -l")
  elif platform.system() == "Darwin":  # macOS
    os.system("pmset displaysleepnow")

def newMeeting():
  webbrowser.open("https://meet.new")

def wordRelations(word, relation_type):
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
          antonyms.update(antonym.name() for antonym in lemma.antonyms())
      return ', '.join(antonyms) if antonyms else "No antonyms found"
    else:
      return "No antonyms found"
  else:
    return "Invalid relation type"

def writeViaKeyboard(text):
  keyboard.write(text)

def voiceTyping():
  a = Listen()
  writeViaKeyboard(a)

def websiteScanner():
  chrome_history_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Profile 1\History"
  history_db_path = os.path.join(os.getcwd(), "ChromeHistoryCopy.txt")
  shutil.copy2(chrome_history_path, history_db_path)
  conn = sqlite3.connect(history_db_path)
  cursor = conn.cursor()
  
  cursor.execute("SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 1")
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

if __name__ == "__main__": print(websiteScanner())