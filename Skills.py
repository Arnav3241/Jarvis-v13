from bs4 import BeautifulSoup
from datetime import datetime
from Functions.Speak import Speak
import webbrowser
import pywhatkit
import requests
  
def googleSearch(query):
  search_url = f"https://www.google.com/search?q={query}"
  webbrowser.open(search_url)
  
def getWeather(location):
  try:
    search_url = f"https://www.google.com/search?q=weather+{location.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    temperature = soup.find("span", attrs={"id": "wob_tm"}).text
    description = soup.find("span", attrs={"id": "wob_dc"}).text
    if location != "":
      weather_info = f"The current temperature in {location} is {temperature}°C with {description}."
    else:
      weather_info = f"The current temperature is {temperature}°C with {description}."
    
    return weather_info
  except:
    return "Couldn't find the weather for that location."

def sendWhatsApp(contact_number, message):
  try: pywhatkit.sendwhatmsg_instantly(phone_no=f"+91{contact_number}", message=message, tab_close=True)
  except: Speak("Couldn't send the message.")




if __name__ == "__main__": 
  a = sendWhatsApp("", "Hello")
  
  print(a)