from pydantic import BaseModel,Field,model_validator
from typing import ClassVar, Optional
import datetime as dt
import os
import json


file_path = "C:\\Users\\richi\\local_website\\folder\\users.txt"

#print(file_size.st_size)
class Identifyer(BaseModel):
    user_id : Optional[int] # well assign user id to users they wont be able to see it |immuntable wi
    password : str    # users will be able to create a password once and then it will be |immutable 
    hashed_id : int   # a hashed id that we will generate the first time that they create an account and will be created using their own password and user id
    class Config:
        allow_mutation = False

   

class Address(BaseModel):
    street: str
    city: str
    zip : int

class users(BaseModel):
    id : Identifyer         # later on implement a non user immutable unquie id
    name : str
    user_name : str
    age: int
    email : str
    is_active : bool
    address :  Optional[str] =   "fisher ave"

    #validates that age isnt below 0
   # @model_validator
    def validate_age(cls, values):
        age = values.get('age')
        if age is not None and age < 0:
            raise ValueError("Age cannot be negative.")
        elif age is None and age < 16:
            raise ValueError("you must be atleast 16 to sign up for this site")
        return values

    def __str__(self):
         return f"objects information name {self.name},age {self.age},email {self.email},is_active {self.is_active},address {self.address}"

    
    def increase_age(self):
         x = self.age
         self.age +=1
         return "you are now one year older", f"was {x} years old, now {self.age} years old"
    
        # checks if two objects are the same by checking there uniquie id's
    def __eq__(self, other) -> bool:
        return (self.id) == (other.id)

import time
""" 
#data = {"people" :[{"name":"richard","age":15,"thing":True},{{"name":"richard","age":15,"thing":True}},{{"name":"richard","age":15,"thing":True}},{{"name":"richard","age":15,"thing":True}}]}
# generator method that yields objects from file
file_path = "C:\\Users\\richi\\local_website\\folder\\users.txt"
#json_string = '{"name": "John Doe", "age": 30, "is_student": true}'
with open(file_path,"r") as file:
        data = file.read()
        js_da = json.loads(data)
        print(type(data),type(js_da))
        for i in range(10):
            print("name: ",js_da["person"][i]["name"],js_da["person"][i]["address"],f"id: {i*2}") # returns name address and id
            time.sleep(5)
"""
def return_sql_data(elm): # returns a list of key value pairs of name id and address for our customers database for test
     file_path = "C:\\Users\\richi\\FastApi\\website\\messageSite\\users.txt"
     with open(file_path,"r") as file:
        data = file.read()
        js_da = json.loads(data)
        #print(type(data),type(js_da))
        result = []
        for i in range(elm):
            name = js_da["person"][i]["name"]
            address = js_da["person"][i]["address"]
            id = f"{i + 14}"  # returns name address and id
            #print(type(js_da["person"][i]["name"])) # return type is string
            result.append({"name":name,"address":address,"id":id})
            #print("iteration", i)
        return result

#name , address , id = return_sql_data(2) # unpacks data 
sql = return_sql_data(3) #stores final list in one object that we can easily access and pass into sql tables
for items in sql: # items is a dictionary
    #print(items)
    name =   items["name"] 
    address = str(items["address"] )
    id  =  int(items["id"])
   
    #print(id)
    """name = items['name']
    address = items["address"]
    id = items["id"]
    str_li = []
    str_li.append(str(name))
    str_li.append(str(address))
    str_li.append(str(id))
    object = str_li[0],str_li[1],str_li[2]
    print(object)
    print(type(object))"""
    #print(type(str_li[0]), type(str_li[1]),type(str_li[2]))


    #print(type(items))
    #dat_json = json.dumps(items)
    #print(dat_json)

    #print(type(dat_json))
    #print(items.keys())
    #name = items['name']
    #address = items["address"]
    #print(name,address)
    """name , address, id = items
    print(name,address,id)"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }