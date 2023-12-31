import string
import random
import hashlib
import ipaddress
from ipaddress import ip_address

import time

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_test_data(num_records):
    test_data = []

    for _ in range(num_records):
        record = {
            "name": generate_random_string(8),
            "age": random.randint(20, 60),
            "email": generate_random_string(10) + "@example.com",
            "is_active": random.choice([True, False]),
            "address": {
                "street": generate_random_string(10),
                "city": generate_random_string(6),
                "zip_code": ''.join(random.choices(string.digits, k=5)),
            }
        }
        test_data.append(record)

    return test_data
import json
#json_ = generate_test_data(50)
#data  = { "person": json_}
file_path = "C:\\Users\\richi\\FastApi\\website\\messageSite\\users.txt"
#with open(file_path,"w") as file:
##   pass
#print(json)
#print(data)
""" 
print(type(json),type(data))
print(data)
print("the data as a whole dictions keys", data.keys())
print("all the keys accsesable by person keys",data["person"][0].keys())"""
def load_json_data_to_dict(file_name):
    with open(file_name,"r") as file:
        data = file.read()
        js_da = json.loads(data)
        print(type(data),type(js_da))
        print(js_da["person"][0].keys()) # returns keys 
        print(js_da) 


#generates a random salt value to add with password before hashing 
def generate_password_salt(val =None ,defualt=True) -> str:
    if defualt:
        salt = generate_random_string(30) + str(random.randint(1,3000)) + generate_random_string(30)
        return salt
    else:
        salt = generate_random_string(val) + str(random.randint(1,3000)) + generate_random_string(val)
        return salt


#stoped here finish checkifng the hashign function
def randompassword(password : str = None):
    if password == None: # if no password is passed in raise a value error
        return ValueError , " you forgot to pass in a password"
    if len(password) > 1: # just for this example but for website password should atleast be 20 chaars long. will validate in pydantic models
        return password.encode("utf-8")

def createRandomPassword(x):
    password = generate_random_string(x)
    return password.encode("utf-8")

# if no password is entered than one is generated. probly wouldnt use in a commercial setting
"""def encodePassword(password: str=None) -> str:
    if password ==  None:
        password = generate_random_string(56).encode("utf-8")
        return password
    return password.encode("utf-8")"""

#implement a hashing function below  # returns hashed value derived from encoded password string and a randomly generated salt
def Hash_salt_andpassword(password : str , salt : str) -> str: # later on append the salt function inside of this to keep things self contained
    #print(type(password))# this of type string .
    passwo = password #password should come in decoded. then decode. pass to a variable along with the salt
    salt_password = str(passwo) + salt 
    hashed_obj =  hashlib.sha1(salt_password.encode("utf-8")) #ecnode the decoded password + salt and hash using SHA-1 algorithm
    hashed_data = hashed_obj.hexdigest()  # returns the value of that hash

    return hashed_data


"""print(type(salt),"  _  ",type(password))"""

# just for example sake prenetend list is mysql data base
 # place holder for data base

def check_password(pas,db) -> bool: # returns true or false if the password exist in database
    salt = generate_password_salt(29)
    hash_value = Hash_salt_andpassword(pas,salt) # computes hash based on inputed password and the salt that is already stored in db that user does not know about
    for i in db: # basic for loop to check evey item in db with this hash function output
        if hash_value in db:
            return True ,"welcome to Texter"
        else:
            return False , "Incorrect password inputed try again"  
        
def validLogin(username:str , password:str) -> bool:
    return True
# actually validate and implement later
import requests
def return_userlocationbasedoffIP(IP):
    Ip_api_key = "9a640087f1ee2d7da2b31c5d918c939c"
    site_ulr = "http://api.ipstack.com/"
    user_IP = str(IP)
    response = requests.get(f"http://api.ipstack.com/{user_IP}?access_key={Ip_api_key}")
    object_countryname = response.json()["country_name"]
    return object_countryname

def is_ip_private(IP): # retuns if inputed ip address is public or private
    return "Private" if (ip_address(IP).is_private) else "Public"