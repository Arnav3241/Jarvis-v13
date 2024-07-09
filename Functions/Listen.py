from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from os import getcwd
import warnings
import os
# import time


warnings.simplefilter("ignore")

os.environ['WDM_LOG'] = '0'
service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(service=service, options=chrome_options)
website = f"{getcwd()}//Functions//HTML//Listen.html"

driver.get(website)

def Listen():
  driver.get(website)
  driver.find_element(by=By.ID, value='start').click()
  print("Listening ...")
  
  while True:
    text = driver.find_element(by=By.ID, value='output').text
    if text != "":
      print(f"You : {text}")
      driver.find_element(by=By.ID, value='end').click()
      return text

if __name__ == "__main__" :
  while True:
    Listen()