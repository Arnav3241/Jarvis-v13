"""
Made by Arnav Singh (https://github.com/Arnav3241) & Avi Sinha (https://github.com/Avi0981) with 💖
"""

from Functions.Speak import Speak as SpeakFunc, TTSK
from firebase_admin import credentials, storage, db
# from Functions.SpeakSync import SpeakSync
# from Functions.Listen import Listen #? Removing Listen as we are already importing it in Skills.js
# from Chat.response import ConversationHistoryManager, Response
from Chat.response import Response
from winotify import Notification
from pygame import mixer
import multiprocessing
import firebase_admin
from Skills import *
import subprocess
import pyautogui
import requests
import pyaudio
import random
import psutil
import serial
import struct
import json
import time
import sys
import eel
import os
import re

# *############# Constants ##############
@eel.expose
def getSoul():
  with open("Interface/Constants/soul.json", "r") as f: soul = json.load(f)
  return soul["soul"]

# *############# Variables ##############

with open('api_keys.json', 'r') as f:
  ld = json.loads(f.read())
  gemini_api_list = ld["gemini_keys"]
  news_api = ld["newsapi"]
  DB_URL = ld["DB_URL"]
  Cred_JSON_Filepath = ld["Cred_JSON_Filepath"]
  storageBucket = ld["storage_bucket"]
  arduino_port = ld["com_port"]

# ? Using a multiprocessing.Value for the shared Exit flag.
Exit = multiprocessing.Value('b', False)
numOfGeminiKeys = len(gemini_api_list)
currentKeyIndex = 0
VoiceExeProcess = None
audio_stream = None
porcupine = None
current_soul = str(getSoul())
pa = None
Soul = getSoul()

@eel.expose
def ChangeGlobalVars(Var, Value):
  global Soul
  if Var == "Soul": Soul = Value
  if Var == "Exit":
    with Exit.get_lock(): Exit.value = Value


@eel.expose
def RefreshGlobalVars(): return [{"Var": "SelectedSoul", "Value": Soul}, {"Var": "Exit", "Value": Exit.value}]

# *############# Basic Functions for running. ##############


def ExecuteCode(code_str: str) -> None:
  try: exec(code_str)
  except Exception as e: print('Error in ExecuteCode function(Execute.py), code contained in input string has wrong syntax OR wrong datatype argument. Error:', e)

def Speak(data):
  Soul = getSoul()
  with open("Interface/History/History.json", "r") as f: history = json.load(f)
  history[str(Soul)]["history"].append({"Data": data, "Date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "Role": "bot"})
  with open("Interface/History/History.json", "w") as f: json.dump(history, f, indent=2)  
  
  SpeakFunc(data)

@eel.expose
def JSprint(data): print("💻 JS: {data}")

@eel.expose
def Terminate():
  with Exit.get_lock(): Exit.value = True
  os._exit(0)


def close(page, sockets_still_open): 
  Soul = getSoul()
  print("Page is closing...")
  try: 
    eel.changeSoul(Soul)
    print("Successfully changed the soul.")
  except Exception as e: print(f"Error in close function(main.py), Error: {e}")

# *############# Home Automation Functions ##############

def LightOn():
  ser.write(b'o')
  print("Ardunio LOG: Lights ON.")

def LightOff():
  ser.write(b'f')
  print("Arduino Log: Lights Off.")

# *############# Some Intitailistaions ##############
ser = None
# history_manager = ConversationHistoryManager()

eel.init("Interface")
mixer.init()

# *############# User History Related Functions ##############


@eel.expose
def AddToUserHistory(data, date, soul, varient="default"):
  if varient == "default":
    print("Adding to history")
    with open("Interface/History/History.json", "r") as f: history = json.load(f)
    with open("Interface/History/History.json", "w") as f:
      history[str(soul)]["history"].append({"Data": data, "Date": str(date), "Role": "user"})
      history[str(soul)]["history"].append({"Data": "skeleton4jaris", "Date": str(date), "Role": "skeleton4jaris"})
      json.dump(history, f, indent=2)


@eel.expose
def AddToUserHistoryImage(data, date, soul, role, img1, img2, img3, img4, varient="default"):
  with open("Interface/History/History.json", "r") as f: history = json.load(f)
  if varient == "default": 
    with open("Interface/History/History.json", "w") as f: history[str(soul)]["history"].append({"Data": data, "Date": date, "Role": role, "Image": [img1, img2, img3, img4]})
  elif varient == "skeleton":
    with open("Interface/History/History.json", "w") as f: history[str(soul)]["history"].append({"Data": data, "Date": date, "Role": role, "Image": []})
  json.dump(history, f, indent=2)


@eel.expose
def DeletePreviousElementFromUserHistory(soul):
  with open("Interface/History/History.json", "r") as f: history = json.load(f)
  with open("Interface/History/History.json", "w") as f:
    history[str(soul)]["history"].pop()
    json.dump(history, f, indent=2)


@eel.expose
def RestoreHistory(soul):
  print("LOG: Restoring history for ", soul)
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)[str(soul)]["history"]
    return history
    # print(history)

# *############# Cache Functions ##############


def UpdateCache(soul):
  with open("Database//Model//Cache//cache.json", "r") as f: cache = json.load(f)
  try: cache = cache[str(soul)]
  except: cache = []

  return cache


def EnterCache(): ...
cache = []


def UploadCache(soul, element):
  with open("Database//Model//Cache//cache.json", "r") as f:
    cache = json.load(f)
  cache[str(soul)].append(element)

  with open("Database//Model//Cache//cache.json", "w") as f: json.dump(cache, f, indent=2)

#*############# Soul's Backend Functions ##############

@eel.expose
def changeSoul(soul):
  with open("Interface/Constants/soul.json", "w") as f: json.dump({"soul": soul}, f, indent=2)
  eel.changeSoul(soul)
  
# *########### GUI Functions ###############

@eel.expose
def eelExecuteQuery(query):
  global currentKeyIndex
  AddToUserHistory(query, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), current_soul)
  t = time.time()
  responseGenCount = 3
  responseGenCountCompletated = 0

  # Bug Fixing
  while responseGenCountCompletated < responseGenCount:
    try:
      res = Response(query, API=gemini_api_list[currentKeyIndex])
      responseGenCountCompletated = 3
      print(res)

      currentKeyIndex += 1

      if currentKeyIndex == numOfGeminiKeys: currentKeyIndex = 0
    except Exception as e: print(f"Error in Response function(Response.py), Error: {e}")
  print(res)
  print(time.time() - t)

  # Return_Output(res, current_soul)
  # eel.funcUpdateChatFromPy()()

  t = time.time()
  # DeletePreviousElementFromUserHistory(current_soul)
  ExecuteCode(res)
  print(time.time() - t)


@eel.expose
def SearchGoogleForJS(query): googleSearch(query)

@eel.expose
def CopyToClipboardForJS(data):
  copyToClipboard(data)
  toastNotification("Jarvis", "Copied to Clipboard", f"Copied '{data}'", "short", f"{os.getcwd()}/Assets/Images/Jarvis.png", False)


@eel.expose
def summarizeText(text):
    prompt = '''Summarize the provided text with the following guidelines:
    1. Give the summary in html tags of <h1>, <p>, and <hr> to make headingings, paragraph, and line breaks.
    2. Use a line division(hr) always after a heading(h1).
    3. Try to use multiple headings in the summary.
    2. Ensure no or minimal loss of data points, preserving all key information.
    3. Maintain objective details with no omissions.
    4. Do not alter the original intent or tone of the text.
    5. Provide the summary without any additional commentary or responses.
    6. THE MOST IMPORTANT INSTRUCTION: THE SUMMARY SHOULD BE LESS WORDS THAN THE INPUT.
    '''
    genai.configure(api_key=gemini_api_list[currentKeyIndex])

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(prompt + f'\n\n\n Based on the instructions above, SUMMARISE THE FOLLOWING TEXT: \n{text}')
    response = response.text
    return response


# *########### Settings Page from GUI functions ###############
def Return_Output(code, soul):
  speak_statements = re.findall(r'Speak\("(.*?)"\)', code)
  single_string = " ".join(speak_statements) 

  with open("Interface/History/History.json", "r") as f: history = json.load(f)
  history[str(soul)]["history"].append({"Data": single_string, "Date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "Role": "bot"})
  with open("Interface/History/History.json", "w") as f: json.dump(history, f, indent=2)


@eel.expose
def ChangeVoice(voice):
  with open("Database/Voice/voice.json", "w") as f: json.dump({"Voice": voice}, f, indent=2)
# ChangeVoice("en-US-SteffanNeural")

# *########### File Reciever Function ###############


toSayWhenRecievedFile = [
  "Received a file, Sir.", 
  "I have received a file, Sir.", 
  "Opening a file that I received, Sir.", 
  "A new file has arrived, Sir.", 
  "I've successfully obtained a file, Sir.",
  "File received, proceeding to open it, Sir.", 
  "The file has been acquired, Sir.", 
  "A file has been added to our system, Sir.", 
  "A document has been delivered, Sir.", 
]

def InititaliseFirebase(cred_json_filepath, db_url, storage_bucket):
  cred = credentials.Certificate(cred_json_filepath)
  firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket, 'databaseURL': db_url})

def DownloadImage(image_url, filename="DownloadedImage.jpg"):
  print("#LOG: Trying to download image...")
  response = requests.get(image_url)

  if response.status_code == 200:
    with open(filename, 'wb') as f: f.write(response.content)
    print("#LOG: Image downloaded successfully!")
  else: print(f"#LOG: Failed to download the image. Status code: {response.status_code}")

  return filename

def DeleteImagesFromFirebase(directory):
  bucket = storage.bucket()
  blobs = bucket.list_blobs(prefix=directory)
  for blob in blobs:
    try:
      blob.delete()
      print(f"Deleted image from Firebase Storage at: {blob.name}")
    except Exception as e: print(f"Failed to delete image from Firebase Storage at: {blob.name}. Error: {e}")

################ MAIN PROCESSES ################

def ImageRecieveAndToDoList(exit_flag, db_url=DB_URL, cred_json_filepath=Cred_JSON_Filepath):
  global Soul, current_soul
  storage_bucket = storageBucket
  InititaliseFirebase(cred_json_filepath, db_url, storage_bucket)
  ref = db.reference('/Link')
  
  def UpdateTasks():
    try:
      global tasks
      with open('todolist.txt', 'r') as f: todolist = f.read()
      tasks = todolist.split('\n')
    except Exception: Speak("Error occurred in function 'UpdateTasks' (in file Skills.py)")

  print("#LOG: Waiting for the image link to be uploaded...")
  while not exit_flag.value:
    current_value = ref.get()
    if current_value != '':
      print(f'#LOG: Current value in the database: {current_value}')
      ref.set('') 

      Speak(random.choice(toSayWhenRecievedFile))
      file_save_path = DownloadImage(current_value, filename=f"{os.getcwd()}/Download/{time.time()}.jpg")
      os.startfile(file_save_path)

      try: DeleteImagesFromFirebase("images/")
      except IndexError: print("#LOG: Failed to extract the correct file path from the URL.")

    UpdateTasks()
    to_delete = []
    for task in tasks:
      if task.split(' ')[0] == IM_getCurrentTime():
        toastNotification("Jarvis To Do", "Task Time", task.split(' ')[1], "long", f"{os.getcwd()}/Assets/Images/Jarvis.png", True)
        to_delete.append(task)

      for task in to_delete: tasks.remove(task)
      if len(to_delete) != 0:
        with open('todolist.txt', 'w') as f:
          for i in range(len(tasks)):
            if i != len(tasks) - 1: 
              f.write(f'{tasks[i]}\n')
              continue
            f.write(f'{tasks[i]}')
    
    # a = getSoul()
    # Soul = a
    # current_soul = a



def funcVoiceExeProcess(exit_flag):
  import pvporcupine

  global ser, audio_stream, porcupine, pa, currentKeyIndex
  with open("Interface/Constants/loaded.json", "w") as f: json.dump({"loaded": True}, f, indent=2)
  SpeakFunc("You can now speak, Sir.")
  
  try: ser = serial.Serial(arduino_port, baud_rate, timeout=1)
  except: print("Arduino not connected.")
  
  time.sleep(1)
  with open("Interface/Constants/loaded.json", "w") as f: json.dump({"loaded": False}, f, indent=2)
  while not exit_flag.value:
    print("\nSpeak now")
    try:
      porcupine = pvporcupine.create(keywords=["jarvis"])
      pa = pyaudio.PyAudio()
      audio_stream = pa.open( rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length )

      while not exit_flag.value:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
          res = ""  # ? Res stands for response.
          # KillExeCodeProcess()
          TTSK()
          Soul = getSoul()
          print("Keyword Detected")
          mixer.music.load("Assets/Audio/Beep.mp3")
          mixer.music.play()

          Query = Listen()
          mixer.music.load("Assets/Audio/Bout.mp3")
          mixer.music.play()
          t = time.time()

          with open(f'{os.getcwd()}\\Database\\Model\\Data\\history.txt', 'a') as f: f.write(f'\nUser: {Query}')
          AddToUserHistory(Query, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), Soul)

          t = time.time()
          a = UpdateCache(Soul)
          print(time.time() - t)

          t = time.time()
          responseGenCount = 3
          responseGenCountCompletated = 0
          

          # Bug Fixing
          while responseGenCountCompletated < responseGenCount:
            print("API being used: ", gemini_api_list[currentKeyIndex])
            try:
              soul = getSoul()
              if soul == "Jarvis": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-EricNeural"}, f, indent=2)
              if soul == "Kakashi_Hatake": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-GuyNeural"}, f, indent=2)
              if soul == "Light_Yagami": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-DavisNeural"}, f, indent=2)
              if soul == "Senku_Ishigami": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-JasonNeural"}, f, indent=2)
              if soul == "Hinata_Hyuga": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-JennyNeural"}, f, indent=2)
              if soul == "Failed_Genious_AI": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-MichelleNeural"}, f, indent=2)
              if soul == "Yui_Hirasawa": 
                with open("Interface/Constants/voice.json", "w") as f: json.dump({"voice": "en-US-AshleyNeural"}, f, indent=2)
              with open(f'{os.getcwd()}\\Database\\Model\\Data\\history.txt', 'r') as f: res = Response(f.read(), Query, API=gemini_api_list[currentKeyIndex], soul=soul)
              responseGenCountCompletated = 3
              print(res)
              currentKeyIndex += 1
              if currentKeyIndex == numOfGeminiKeys: currentKeyIndex = 0
            except Exception as e:
              print(f"Error in Response function(Response.py), Error: {e}")
              currentKeyIndex += 1
              responseGenCountCompletated += 1
          print(time.time() - t)

          t = time.time()
          DeletePreviousElementFromUserHistory(Soul)

          if "EnterCache()" in res:
            lines = res.split('\n')
            filtered_lines = [line for line in lines if "EnterCache()" not in line]
            res = '\n'.join(filtered_lines)
            UploadCache(Soul, { "input": Query, "output": f"{str(res)}" })

          ExecuteCode(res)
          print(time.time() - t)

    finally:
      if porcupine is not None: porcupine.delete()
      if audio_stream is not None: audio_stream.close()
      if pa is not None: pa.terminate()


def funcGUIprocess():
    toast = Notification(app_id="Jarvis", title="Jarvis is Up and Ready.", msg="Sir, your personal assistant Jarvis is up and is willing to do anything you want.", duration="short", icon=f"{os.getcwd()}/Assets/Images/Jarvis.png")
    toast.show()

    VoiceExeProcess = multiprocessing.Process(target=funcVoiceExeProcess, args=(Exit,))
    VoiceExeProcess.start()

    ImageRecieveAndToDoListUpdateProcess = multiprocessing.Process(target=ImageRecieveAndToDoList, args=(Exit,))
    ImageRecieveAndToDoListUpdateProcess.start()

    try: eel.start("loading.html", position=(0, 0), close_callback=close, block=True, size=(1500, 1200), port=8080)
    except Exception as e:
      print(f"\n💀: Jarvis has encountered a fatal error. Please try later. Error: {e}")
      with Exit.get_lock(): Exit.value = True

    if Exit.value:
      VoiceExeProcess.terminate()
      VoiceExeProcess.join()
      os._exit(0)


if __name__ == "__main__":
    funcGUIprocess()