import requests
import json
from pprint import pprint


response = requests.get("http://127.0.0.1:8000/todo")


pprint(response.json())
print(type(response.content))
print("new change")
