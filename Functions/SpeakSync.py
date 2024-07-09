import subprocess

def SpeakSync(*args):
  global process
  audio = ""
  for i in args:
    audio += str(i)
  
  audio = audio.replace('"', "")
  audio = audio.replace('*', "dash ")

  with open("Database//Speak//Speak.txt", "w") as file:
    file.write(audio)
  subprocess.run(["python", "Utils//RunTTS.py"])

def TTSK():
  process.kill()
  print("Speech Process Terminated")

if __name__ == "__main__":
  while True:
    SpeakSync(input(">>> "))

#? Author - Arnav Singh (https://github.com/Arnav3241)