from playsound import playsound
import pyttsx3
import os

Model = pyttsx3.init('sapi5')
Model.setProperty('rate', 180)

# Online
def Speak1(text, voice="en-US-SteffanNeural"):
  if text == "": return
  command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{os.getcwd()}\\Assets\\Audio\\TTS.mp3"'
  os.system(command)
  
  playsound("Assets/Audio/TTS.mp3")
  
# Offline
def Speak2(text):  
  Model.say(text)
  print(f"Jarvis : {text}")
  Model.runAndWait()

def RunTTS(text, voice="en-US-SteffanNeural"):
  # try: Speak1(text) 
  # except: Speak2(text)
  if voice == "en-default-DavidNeural": Speak2(text, "en-US-DavidNeural")
  else: Speak1(text, voice)
  

with open('Database//Speak//Speak.txt', 'r') as file:
  contents = file.read()
  RunTTS(contents)

#? Author - Arnav Singh (https://github.com/Arnav3241)