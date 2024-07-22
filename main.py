# from Functions.Speak import Speak
# from Functions.SpeakSync import SpeakSync
# from Tests.r1 import Response
# from Functions.Listen import Listen

# while True: 
#   a = Response(Listen())
#   print(a)
#   try: print(a)
#   except: SpeakSync("I'm sorry, I didn't get that.")

import json
import eel

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

def on_close(page, sockets):
	print(page, 'closed')
	print('Still have sockets open to', sockets)

if __name__ == '__main__': 
  try: 
    eel.start("index.html", size=(1500, 1200), position=(0, 0), callback=on_close) 
  except:
    print(f"\n💀: Jarvis has encountered a fatal error. Please try later.")
    exit()

# AddToUserHistory("Hello", "12/12/2021", "1")
# print(RestoreHistory("1"))