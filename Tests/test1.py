import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser

# Initialize the speech engine
engine = pyttsx3.init()

# Define the Speak function
def Speak(text):
    engine.say(text)
    engine.runAndWait()

Speak("Okay buddy, opening chrome, insta, twitter, amazon, pw.com, word, excel, trello, slides, and powerpoint for you. Anything else you need, just let me know!")
webbrowser.open("https://www.google.com/chrome/")
webbrowser.open("https://www.instagram.com/")
webbrowser.open("https://twitter.com/")
webbrowser.open("https://www.amazon.in/")
webbrowser.open("https://pw.live/")
webbrowser.open("https://www.microsoft.com/en-in/microsoft-365/word")
webbrowser.open("https://www.microsoft.com/en-in/microsoft-365/excel")
webbrowser.open("https://trello.com/")
webbrowser.open("https://www.google.co.in/slides/about/")
webbrowser.open("https://www.microsoft.com/en-in/microsoft-365/powerpoint")
Speak("I can also search for the best jeans for you on Amazon and Flipkart. What kind of jeans are you looking for? Slim fit, ripped, bootcut? And what's your budget?")