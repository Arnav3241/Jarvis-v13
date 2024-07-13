import time
import os
import joblib
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY=os.environ.get("API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f'{time.time()}'

try:
  os.mkdir('data/')
except:
  # data/ folder already exists
  pass

# Load past chats (if available)
try:
  past_chats: dict = joblib.load('data/past_chats_list')
except:
  past_chats = {}

