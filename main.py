from Functions.Speak import Speak
from Functions.SpeakSync import SpeakSync
from Tests.r1 import Response
from Functions.Listen import Listen

while True: 
  a = Response(Listen())
  print(a)
  try: exec(a)
  except: SpeakSync("I'm sorry, I didn't get that.")

# import eel

# #? Some important inits
# eel.init("Interface")

# if __name__ == '__main__': 
#   try: 
#     eel.start("index.html", mode='chrome', size=(1500, 1200), position=(0, 0)) 
#   except: 
#     print("\n💀: Jarvis has encountered a fatal error. Please try later.")
#     exit()