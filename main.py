"""
Made by Arnav Singh (https://github.com/Arnav3241) & Avi Sinha (https://github.com/Avi0981) with 💖
"""

from Functions.Speak import Speak as SpeakFunc, TTSK
from firebase_admin import credentials, storage, db
# from Functions.SpeakSync import SpeakSync
from Functions.Listen import Listen
from Chat.response import Response
from winotify import Notification
from urllib.parse import unquote
from pygame import mixer  
import multiprocessing
import firebase_admin
from Skills import *
import pvporcupine
import requests
import pyaudio
import random
import struct
import json
import time
import eel
import os
import re

def ExecuteCode(code_str: str) -> None:
  try:
    exec(code_str)
  except Exception as e:
    print('Error in ExecuteCode function(Execute.py), code contained in input string has wrong syntax OR wrong datatype argument. Error:', e)

#? Some important inits
eel.init("Interface")
mixer.init()

@eel.expose
def AddToUserHistory(data, date, soul, varient="default"):
  if varient == "default":
    print("Adding to history")
    with open("Interface/History/History.json", "r") as f:
      history = json.load(f)
        
    with open("Interface/History/History.json", "w") as f:
      history[str(soul)]["history"].append({
        "Data": data,
        "Date": str(date),
        "Role": "user"
      })      
      history[str(soul)]["history"].append({
        "Data": "skeleton4jaris",
        "Date": str(date),
        "Role": "skeleton4jaris"
      })
      json.dump(history, f, indent=2)  
  

@eel.expose
def AddToUserHistoryImage(data, date, soul, role, img1, img2, img3, img4, varient="default"):
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    
  if varient == "default":
    with open("Interface/History/History.json", "w") as f:
      history[str(soul)]["history"].append({
        "Data": data,
        "Date": date,
        "Role": role,
        "Image": [
          img1, img2, img3, img4          
        ]
      })
  elif varient == "skeleton":
    with open("Interface/History/History.json", "w") as f:
      history[str(soul)]["history"].append({
        "Data": data,
        "Date": date,
        "Role": role,
        "Image": []
      })
    
    json.dump(history, f, indent=2)

def DeletePreviousElementFromUserHistory(soul):
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    
  with open("Interface/History/History.json", "w") as f:
    history[str(soul)]["history"].pop()
    json.dump(history, f, indent=2)
    
@eel.expose
def RestoreHistory(soul):
  print("Restoring history for ", soul)
  
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    # print(history)
    return history[str(soul)]["history"]  

def Return_Output(code, soul):
  speak_statements = re.findall(r'Speak\("(.*?)"\)', code)
  single_string = " ".join(speak_statements)
  
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    
  history[str(soul)]["history"].append({
    "Data": single_string,
    "Date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "Role": "bot"
  })
  
  with open("Interface/History/History.json", "w") as f:
    json.dump(history, f, indent=2)


@eel.expose
def ChangeVoice(voice): 
  with open("Database/Voice/voice.json", "w") as f:
    json.dump({"Voice": voice}, f, indent=2)
# ChangeVoice("en-US-SteffanNeural")

#? Global Vars
MainExeStarted = False
ChatDissabled = False
Speaking = False
GenResponse = False
Soul = 1
SelectedSoul = ""
Exit = multiprocessing.Value('b', False)  #? Using a multiprocessing.Value for the shared Exit flag.
#  = multiprocessing.Value('b', False)  

#? Local Vars
VoiceExeProcess = None
audio_stream = None
porcupine = None
pa = None

#? Import Variables
with open('api_keys.json', 'r') as f:
  ld = json.loads(f.read())
  gemini_api = ld["gemini1"]
  news_api = ld["newsapi"]
  DB_URL = ld["DB_URL"]
  Cred_JSON_Filepath = ld["Cred_JSON_Filepath"]
  storageBucket = ld["storage_bucket"]
  

def Speak(data):
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    
  history[str(Soul)]["history"].append({
    "Data": data,
    "Date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "Role": "bot"
  })
  
  with open("Interface/History/History.json", "w") as f:
    json.dump(history, f, indent=2)
    
  SpeakFunc(data)

@eel.expose
def ChangeGlobalVars(Var, Value):
  global MainExeStarted, ChatDissabled, Speaking, GenResponse, SelectedSoul
  if Var == "MainExeStarted": MainExeStarted = Value
  if Var == "ChatDissabled": ChatDissabled = Value
  if Var == "Speaking": Speaking = Value
  if Var == "GenResponse": GenResponse = Value
  if Var == "SelectedSoul": SelectedSoul = Value
  if Var == "Exit": 
    with Exit.get_lock():
      Exit.value = Value

@eel.expose
def RefreshGlobalVars():
  return [
    {"Var": "MainExeStarted", "Value": MainExeStarted},
    {"Var": "ChatDissabled", "Value": ChatDissabled},
    {"Var": "Speaking", "Value": Speaking},
    {"Var": "GenResponse", "Value": GenResponse},
    {"Var": "SelectedSoul", "Value": SelectedSoul},
    {"Var": "Exit", "Value": Exit.value}
  ]

#? Recieving Image from Firebase - Functions

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
  firebase_admin.initialize_app(cred, {
    'storageBucket': storage_bucket,
    'databaseURL': db_url
  })
  
def DownloadImage(image_url, filename="DownloadedImage.jpg"):
  print("#LOG: Trying to download image...")
  response = requests.get(image_url)
  
  if response.status_code == 200:
    with open(filename, 'wb') as f:
      f.write(response.content)
    print("#LOG: Image downloaded successfully!")
  else:
    print(f"#LOG: Failed to download the image. Status code: {response.status_code}")
    
  return filename

def DeleteImagesFromFirebase(directory):
  bucket = storage.bucket()
  blobs = bucket.list_blobs(prefix=directory)
  for blob in blobs:
    try:
      blob.delete()
      print(f"Deleted image from Firebase Storage at: {blob.name}")
    except Exception as e:
      print(f"Failed to delete image from Firebase Storage at: {blob.name}. Error: {e}")
    

@eel.expose
def PPPrint(data):
  print("💻 JS: {data}")

@eel.expose
def Terminate():
  with Exit.get_lock():
    Exit.value = True
  os._exit(0)

def close(page, sockets_still_open):
  print("Page is closing...")




def ImageFirebaseLink(exit_flag, db_url=DB_URL, cred_json_filepath=Cred_JSON_Filepath):
  storage_bucket = storageBucket
  InititaliseFirebase(cred_json_filepath, db_url, storage_bucket)
  ref = db.reference('/Link')
  
  print("#LOG: Waiting for the image link to be uploaded...")
  
  while not exit_flag.value:
    current_value = ref.get()
    if current_value != '':
      print(f'#LOG: Current value in the database: {current_value}')
      ref.set('')  # Reset the database reference
      
      Speak(random.choice(toSayWhenRecievedFile))
      file_save_path = DownloadImage(current_value, filename=f"{os.getcwd()}/Download/{time.time()}.jpg")
      os.startfile(file_save_path)
      
      try: 
        firebase_file_path = current_value.split("/o/")[1].split("?")[0]
        firebase_file_path = unquote(current_value.split(storage_bucket)[1])
        DeleteImagesFromFirebase("images/")
      except IndexError: print("#LOG: Failed to extract the correct file path from the URL.")

def funcVoiceExeProcess(exit_flag): 
  SpeakFunc("You can now speak, Sir.")
  while not exit_flag.value: 
    print("\nSpeak now")
    try:
      porcupine = pvporcupine.create(keywords=["jarvis"])
      pa = pyaudio.PyAudio()
      audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
      )

      while not exit_flag.value: 
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
          TTSK()
          print("Keyword Detected")
          mixer.music.load("Assets/Audio/Beep.mp3")
          mixer.music.play()
          
          Query = Listen()          
          mixer.music.load("Assets/Audio/Bout.mp3")
          mixer.music.play()
          t = time.time()
          AddToUserHistory(Query, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "1")  
          
          print(time.time() - t)
          
          t = time.time()
          res = Response(Query, API=gemini_api)
          print(res)
          print(time.time() - t)
            
          # Return_Output(res, "1")
          # eel.funcUpdateChatFromPy()()

          t = time.time()
          DeletePreviousElementFromUserHistory("1")
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
  
  ImageRecieveProcess = multiprocessing.Process(target=ImageFirebaseLink, args=(Exit,))
  ImageRecieveProcess.start()
  
  try:
    eel.start("index.html", position=(0, 0), close_callback=close, block=True, size=(1500, 1200), port=8080)
    
  except Exception as e:
    print(f"\n💀: Jarvis has encountered a fatal error. Please try later. Error: {e}")
    with Exit.get_lock():
      Exit.value = True

  if Exit.value:
    VoiceExeProcess.terminate()
    VoiceExeProcess.join()
    os._exit(0)

if __name__ == "__main__":
  funcGUIprocess()