from playsound import playsound
import pyttsx3
import json
import os
 
Model = pyttsx3.init('sapi5')
Model.setProperty('rate', 180)
def getCurrentVoice():
  with open("Interface/Constants/voice.json", "r") as f: voice = json.load(f)
  return voice["voice"]

# Online
def Speak1(text, voice="en-US-EricNeural"):
  if text == "": return
  command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{os.getcwd()}\\Assets\\Audio\\TTS.mp3"'
  os.system(command)
  playsound(f"Assets/Audio/TTS.mp3")
  
# Offline
def Speak2(text):  
  Model.say(text)
  print(f"Jarvis : {text}")
  Model.runAndWait()

# print(getCurrentVoice())

def RunTTS(text, voice="en-US-EricNeural"):
  # try: Speak1(text) 
  # except: Speak2(text)
  if voice == "en-default-DavidNeural": Speak2(text)
  else: Speak1(text, voice)
  

with open('Database//Speak//Speak.txt', 'r') as file:
  contents = file.read()
  RunTTS(contents, getCurrentVoice())



#? Author - Arnav Singh (https://github.com/Arnav3241)