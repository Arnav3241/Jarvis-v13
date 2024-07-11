import json
import os
import time

Cache = []
file = r"Cache/Cache.json"

def Response(input):  
  input = input.lower()
  global Cache
  
  if os.path.exists(file):
    with open(file, 'r') as fData: 
      Cache = json.load(fData)
      if Cache == "": Cache = {}
  else: Cache = []
  
  for element in Cache:
    if element["input"] == input:
      return element["output"]
  
  #? Make he resonose system here
  time.sleep(2)
  response = input
  
  Cache.append({"input": input, "output": response})
  with open(file, 'w') as fData:
    json.dump(Cache, fData)
  
  return response

while True:
  print(Response(input("Enter: ")))