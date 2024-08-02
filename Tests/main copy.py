# from Functions.Speak import Speak
# from Functions.SpeakSync import SpeakSync
# from Tests.r1 import Response
# from Functions.Listen import Listen

# while True: 
#   a = Response(Listen())
#   print(a)
#   try: print(a)
#   except: SpeakSync("I'm sorry, I didn't get that.")

import multiprocessing
import json
import sys
import time
import eel
import os
from Functions.SpeakSync import SpeakSync

#? Some important inits
eel.init("Interface")

@eel.expose
def AddToUserHistory(data, date, soul, role):
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    
  with open("Interface/History/History.json", "w") as f:
    history[str(soul)]["history"].append({
      "Data": data,
      "Date": date,
      "Role": role
    })
    json.dump(history, f, indent=2)    

@eel.expose
def RestoreHistory(soul):
  print("Restoring history for ", soul)
  
  with open("Interface/History/History.json", "r") as f:
    history = json.load(f)
    print(history)
    return history[str(soul)]["history"]
  
#? Global Vars
MainExeStarted = False
ChatDissabled = False
Speaking = False
GenResponse = False
SelectedSoul = ""
Exit = False

@eel.expose
def ChangeGlobalVars(Var, Value):
  global MainExeStarted, ChatDissabled, Speaking, GenResponse, SelectedSoul, Exit
  if Var == "MainExeStarted": MainExeStarted = Value
  if Var == "ChatDissabled": ChatDissabled = Value
  if Var == "Speaking": Speaking = Value
  if Var == "GenResponse": GenResponse = Value
  if Var == "SelectedSoul": SelectedSoul = Value
  if Var == "Exit": Exit = Value

@eel.expose
def RefreshGlobalVars():
  return [
    {"Var": "MainExeStarted", "Value": MainExeStarted},
    {"Var": "ChatDissabled", "Value": ChatDissabled},
    {"Var": "Speaking", "Value": Speaking},
    {"Var": "GenResponse", "Value": GenResponse},
    {"Var": "SelectedSoul", "Value": SelectedSoul},
    {"Var": "Exit", "Value": Exit}
  ]

@eel.expose
def PPPrint(data):
  print(data)

@eel.expose
def Terminate():
  global Exit
  Exit = True
  
def close(page, sockets_still_open):
  global Exit
  Exit = True
  os._exit(0)
  
# @eel.expose
# def MainExecution():
#   while Exit == False:
#     print(f"Value of Exit: {Exit}")
#     time.sleep(1)

def funcVoiceExeProcess(): 
  if __name__ == "__main__":
    while True:
      SpeakSync("VoiceExeProcess running...")
      # time.sleep(1)

def funcGUIprocess(): 
  global Exit
  
  try:
    eel.start("index.html", size=(1500, 1200), position=(0, 0), close_callback=close)
    
    VoiceExeProcess = multiprocessing.Process(target=funcVoiceExeProcess)
    VoiceExeProcess.start()
    
    if Exit == True:
      print("VoiceExeProcess terminated.")
      VoiceExeProcess.terminate()
      VoiceExeProcess.join()
      print("GUIprocess terminated.")
      exit()    
    
  except:
    print(f"\n💀: Jarvis has encountered a fatal error. Please try later.")
    exit()

# def funcVoiceExeProcess(): 
#   while True:
#     print("VoiceExeProcess running...")
#     time.sleep(1)
  # global Exit
  
  # GUIprocess = multiprocessing.Process(target=funcGUIprocess)
  # GUIprocess.start()
  
  # print("VoiceExeProcess running...")
  # while Exit == False:
  #   if Exit == True:
  #     GUIprocess.terminate()
  #     GUIprocess.join()
  #     print("GUIprocess terminated.")
  #     print("VoiceExeProcess terminated.")
  #     break
  #   else: 
  #     print("hi")  
  #     time.sleep(1/2)
    
  

# if __name__ == '__main__': 
#   try: 
#     eel.start("index.html", size=(1500, 1200), position=(0, 0), close_callback=close) 
#   except:
#     print(f"\n💀: Jarvis has encountered a fatal error. Please try later.")
#     exit()

if __name__ == "__main__":
  funcGUIprocess()
