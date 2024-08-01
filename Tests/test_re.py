import re

code = """
Speak("Hey dude, I'm doing fantastic, thanks for asking!. Always happy to help a friend out.")
Speak("Opening Chrome for you, bro. Hope you are going to do something productive today.")
webbrowser.open("https://www.google.com/")
Speak("Opening File Explorer.  Let's see what you've got in store!.")
os.system("start explorer")
Speak("Photosynthesis is like, plants using sunlight to make their own food, man. They're like, the ultimate chefs using light, water, and carbon dioxide to cook up some delicious glucose.")
Speak("The atomic number of sulfur is 16, my friend. Remember that!.")
Speak("Okay, opening Amazon and Flipkart for you. Hope you find the perfect keyboard under 3,000 rupees!. Let me know if you want me to sort it by anything")
webbrowser.open("https://www.amazon.in/s?k=best+keyboard+under+3000+rupees")
webbrowser.open("https://www.flipkart.com/search?q=best+keyboard+under+3000+rupees")
"""

# Extract Speak statements
speak_statements = re.findall(r'Speak\("(.*?)"\)', code)

# Return the list of Speak statements
print(speak_statements)