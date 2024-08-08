"""
Made by Arnav Singh (https://github.com/Arnav3241) & Avi Sinha (https://github.com/Avi0981) with 💖
"""

from Functions.SpeakSync import SpeakSync
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

arduino_port = 'COM3'  
baud_rate = 9600  

try: from nltk.corpus import wordnet
except: nltk.download('wordnet')

with open('api_keys.json', 'r') as f:
  ld = json.loads(f.read())
  api = ld["gemini1"]
  news_api = ld["newsapi"]

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
  except: SpeakSync("Couldn't send the message.")

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

def checkInternetSpeed():
  st = speedtest.Speedtest()
  download_speed = st.download() / 1_000_000  # Convert to Mbps
  upload_speed = st.upload() / 1_000_000  # Convert to Mbps
  return int(download_speed), int(upload_speed)

def getPublicIP():
  ip = requests.get("https://api.ipify.org").text
  return ip

def getLocalIP():
  hostname = socket.gethostname()
  local_ip = socket.gethostbyname(hostname)
  return local_ip

def searchWikipedia(query):
  summary = wikipedia.summary(query, sentences=2)
  return summary

def getCryptoPrice(crypto="bitcoin"):
  url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd'
  response = requests.get(url)
  data = response.json()
  return data[crypto]['usd']

def searchAndOpen(product_name):
  product_name = urllib.parse.quote_plus(product_name)
    
  webbrowser.open(f"https://www.amazon.com/s?k={product_name}")
  webbrowser.open(f"https://www.ebay.com/sch/i.html?_nkw={product_name}")
  webbrowser.open(f"https://www.flipkart.com/search?q={product_name}")

def textSummarisation(text):
  model = genai.GenerativeModel('gemini-1.5-pro-latest')
  responseAI = model.generate_content(f"""
    {text}
    
    QUERY : Given above is a piece of text.
    Summarize this text in a few words without omitting any key points of the text.
  """)

  return responseAI.text

def getNews():
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
  
  if response.status_code != 200: print(f"Error: {response.status_code}, Message: {response.text}")
  else:
    data = response.json()
    if 'articles' in data and data['articles']:
      a = 10
      b = 0
      for article in data['articles']: 
        news_str += f"{article['title']}: {article['description']}\n\n"
        urls.append(article['url'])
        b = b + 1
        if b == a: break
    else: news_str = "No articles found."

  return news_str, urls


def toastNotification(app_id, title, msg, duration, icon, loop):
  toast = Notification(app_id=app_id, title=title, msg=msg, duration=duration, icon=icon)
  
  if loop: toast.set_audio(audio.LoopingCall, loop=True)
  else: toast.set_audio(audio.Default, loop=False)
  
  toast.show()


################### NOT TO BE USED BY GEMINI #######################

def __IM_getCurrentTime():
  current_time = datetime.now()
  hour = current_time.strftime("%I").lstrip('0')  # Remove leading zero from hour
  minute = current_time.strftime("%M")
  formatted_time = f"{hour}:{minute}"
  return formatted_time

def __UpdateTasks():
  global tasks
  with open('todolist.txt', 'r') as f:
    todolist = f.read()
  tasks = todolist.split('\n')


#######################################################################

################### TO-DO LIST FUNCTIONS ###########################

TDL_ACTIVE = False
tasks = []

def TDL_activate():
  global TDL_ACTIVE
  TDL_ACTIVE = True

  def daemonTask():
    while TDL_ACTIVE:
      __UpdateTasks()

      to_delete = []
      for task in tasks:
        if task.split(' ')[0] == __IM_getCurrentTime():
          toastNotification("Jarvis Todo", "Task time!", task.split(' ')[1], "long", f"{os.getcwd()}/Assets/Images/Jarvis.png", True)
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

def TDL_deactivate():
  global TDL_ACTIVE
  TDL_ACTIVE = False

def TDL_add(hours, minutes, task_name):
  with open('todolist.txt', 'a') as f:
    f.write(f'\n{hours}:{minutes} {task_name}')

def TDL_show():
  os.system(f"notepad.exe {os.getcwd()}/todolist.txt")

###################################################################




if __name__ == "__main__":
  # LightOn()
  TDL_show()
  while True:
    pass
  TDL_add(3, 19, 'study')

  # TDL_show()
  # TDL_activate()
  # while True:
  #   pass