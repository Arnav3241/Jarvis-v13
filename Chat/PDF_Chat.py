from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import google.generativeai as genAI
from langchain_chroma import Chroma
import shutil
import signal
import json
import sys
import os

try: shutil.rmtree(f"{os.getcwd()}//chroma_db_nccn")
except Exception as e: print(e)

loaders = [PyPDFLoader(fr'{input("Enter the path of the PDF file: ")}')]
docs = []

print("Loading PDF file...")

def signal_handler(sig, frame):
  print('\nThanks for using Gemini. :)')
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

for file in loaders:
  docs.extend(file.load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db_nccn")

print("File Loaded")

# Import Variables
with open('api_keys.json', 'r') as f:
  ld = json.loads(f.read())
  API = ld["gemini1"]

genAI.configure(api_key=API)
model = genAI.GenerativeModel(model_name='gemini-pro')

def genRAGprompt(query, context):
  context = context.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = ("You are a helpful and informative bot designed to answer questions using text from PDF documents. Your goal is to provide complete and comprehensive responses, ensuring clarity and accuracy. However, keep in mind that you are addressing a non-technical audience, so make sure to break down complex information into simple and easy-to-understand language. Use a friendly and conversational tone to make the information more engaging and accessible. If the context is irrelevant to the answer, you may ignore it. Focus on providing the most relevant and useful information based on the user's query. QUESTION: '{query}'  CONTEXT: '{context}' ANSWER: ").format(query=query, context=context)
  return prompt

def generate_answer(prompt):
  answer = model.generate_content(prompt)
  return answer.text

def getReleventContextFromDB(query):
  context = ""
  embeddings_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L6-v2", model_kwargs={"device": "cpu"})
  vector_db = Chroma(persist_directory="./chroma_db_nccn")
  vector_db._embedding_function = embeddings_function
  
  search_results = vector_db.similarity_search(query, k=6)
  for result in search_results:
    context += result.page_content + "\n"
  return context

if __name__ == "__main__":
  while True:
    print("-----------------------------------")
    query = input("Enter a query: ")
    context = getReleventContextFromDB(query)
    prompt = genRAGprompt(query=query, context=context)
    print(generate_answer(prompt=prompt))
