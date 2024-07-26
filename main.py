from win10toast import ToastNotifier
import multiprocessing
import webview
import json
import time
import eel
import os

#? Some important inits
eel.init("Interface")

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
  print(data)

@eel.expose
def Terminate():
  with Exit.get_lock():
    Exit.value = True
  os._exit(0)

def close(page, sockets_still_open):
  print("Page is closing...")

def funcVoiceExeProcess(exit_flag): 
  notify = ToastNotifier()
  notify.show_toast("Jarvis", "Jarvis is now up and running.", duration=10, icon_path=r"icon.ico", threaded=True)
  
  while not exit_flag.value:
    print("VoiceExeProcess running...")
    time.sleep(1)

def funcGUIprocess(): 
  VoiceExeProcess = multiprocessing.Process(target=funcVoiceExeProcess, args=(Exit,))
  VoiceExeProcess.start()
  
  try:
    # eel.start("index.html", size=(1500, 1200), position=(0, 0), close_callback=close, block=True)
    eel.start("index.html", position=(0, 0), close_callback=close, block=True, size=(1920, 1080), cmdline_args=['--start-fullscreen'])
    
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
