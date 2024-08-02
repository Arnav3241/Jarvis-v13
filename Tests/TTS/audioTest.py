from playsound import playsound
import pyttsx3
import os

Model = pyttsx3.init('sapi5')
Model.setProperty('rate', 180)

# Online
def Speak1(text, voice="en-US-JennyNeural"):
  if text == "": return
  command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{os.getcwd()}\\Tests\\{voice}.mp3"'
  # command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{os.getcwd()}\\Tests\\{voice}.mp3"  --rate +25% --pitch +300Hz'
  os.system(command)
  
  
# Offline
def Speak2(text):  
  Model.say(text)
  print(f"Jarvis : {text}")
  Model.runAndWait()

def RunTTS(text):
  # try: Speak1(text) 
  # except: Speak2(text)
  Speak1(text)

with open('Database//Speak//Speak.txt', 'r') as file:
  contents = file.read()
  RunTTS(contents)

#? Author - Arnav Singh (https://github.com/Arnav3241)