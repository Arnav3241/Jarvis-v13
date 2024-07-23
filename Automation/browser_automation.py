'''
Author: Avi Sinha (https://github.com/Avi0981)
'''

from pyautogui import *
import time

PAUSE = 0.2

def open_chrome():
    press('win')
    time.sleep(0.3)
    typewrite('google chrome')
    time.sleep(0.3)
    press('enter')

def google_search(query):
    open_website('google.com')
    time.sleep(2)
    typewrite(query)
    time.sleep(0.3)
    press('enter')

def google_and_open_first_website(query):
    google_search(query)
    time.sleep(10) # Buffer time
    hotkey('ctrl', 'shift', 'i')
    time.sleep(7)
    click(1600, 810)
    click(1600, 810)
    typewrite('document.querySelectorAll(\'.g a\')[0].click();')
    time.sleep(0.3)
    press('enter')
    time.sleep(0.3)
    hotkey('ctrl', 'shift', 'i')

def open_website(url):
    hotkey('ctrl', 't')
    time.sleep(0.3)
    typewrite(url)
    time.sleep(0.3)
    press('enter')

if __name__ == '__main__':
    open_chrome()
    time.sleep(2)
    google_and_open_first_website('tcs')
