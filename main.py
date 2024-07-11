# from Functions.Speak import Speak
# from Functions.SpeakSync import SpeakSync
# from Functions.Listen import Listen

# while True:
#   SpeakSync(Listen())

import eel

#? Some important inits
eel.init("Interface")

if __name__ == '__main__': 
  try: 
    eel.start("index.html", mode='chrome', size=(1500, 1200), position=(0, 0)) 
  except: 
    print("\n💀: Jarvis has encountered a fatel error. Please try later.")
    exit()