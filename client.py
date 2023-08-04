import requests
import json
from pprint import pprint
import time

for i in range(10):
    response = requests.get("http://127.0.0.1:8000/todo") # can use .text also
    time.sleep(10)

