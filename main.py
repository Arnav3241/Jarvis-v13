"""
Made by Arnav Singh (https://github.com/Arnav3241) with 💖
"""

# from win10toast import ToastNotifier
from Functions.SpeakSync import SpeakSync
from Functions.Listen import Listen
from pygame import mixer  
import multiprocessing
import pvporcupine
import keyboard
import pyaudio
import struct
import json
import time
import eel
import os

#? Some important inits
eel.init("Interface")

mixer.init()

@eel.expose
def AddToUserHistory(data, date, soul, role):
  with open("Database/History/History.json", "r") as f:
    history = json.load(f)
    
  with open("Database/History/History.json", "w") as f:
    history[str(soul)]["history"].append({
      "Data": data,
      "Date": date,
      "Role": role
    })
    json.dump(history, f, indent=2)    

@eel.expose
def RestoreHistory(soul):
  print("Restoring history for ", soul)
  
  with open("Database/History/History.json", "r") as f:
    history = json.load(f)
    print(history)
    return history[str(soul)]["history"]
  
#? Global Vars
MainExeStarted = False
ChatDissabled = False
Speaking = False
GenResponse = False
SelectedSoul = ""
Exit = multiprocessing.Value('b', False)  # Use a multiprocessing.Value for the shared Exit flag

#? Local Vars
VoiceExeProcess = None
audio_stream = None
porcupine = None
pa = None

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

def funcVoiceExeProcess(exit_flag): 
  # notify = ToastNotifier()
  # notify.show_toast("Jarvis", "Jarvis is now up and running.", duration=10, icon_path=r"E:\\Jarvis-v13\\icon.ico", threaded=True)
  
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
          print("Keyword Detected")
          mixer.music.load("Assets/Audio/Beep.mp3")
          mixer.music.play()
          
          Query = Listen()          
          mixer.music.load("Assets/Audio/Bout.mp3")
          mixer.music.play()
          
          AddToUserHistory(Query, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "1", "user")
          SpeakSync(Query)
        else:
          print("Keyword not detected")
        
    finally: 
      if porcupine is not None: porcupine.delete()
      if audio_stream is not None: audio_stream.close()
      if pa is not None: pa.terminate()
  

def funcGUIprocess(): 
  VoiceExeProcess = multiprocessing.Process(target=funcVoiceExeProcess, args=(Exit,))
  VoiceExeProcess.start()
  
  try:
    eel.start("index.html", position=(0, 0), close_callback=close, block=True, size=(1920, 1080), port=8080)
    
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
