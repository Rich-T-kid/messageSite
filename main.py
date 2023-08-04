from fastapi import FastAPI ,Form , Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, Response
from typing import ClassVar
from fastapi.staticfiles import StaticFiles
import random
from datetime import date
import time
import datetime
from typing import Optional
from pydantic import BaseModel , Json , Field
import ipaddress


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templats = Jinja2Templates(directory="templates")
today = date.today()

todos = [
{
    "id" : "1","activity": "jogging for two hours at a time"},{"id":"2","activity":"writing 3 pages for my college class at 3 am"}
]
#for post request using data
user_data = []
#for post request using book reviews
book_reviews = []
# storing messages
messages = []
# models below
class userModel(BaseModel):
   id : int
   name : str | None = None
  
   is_active : bool
   activities : list | None = None
    
class post(BaseModel):
    id : int
    title: str
    content : str
    publised : bool 
    date_of_post : date = Field(default=date.today()) # returns todays date by defualt with every post request 
    rating: Optional[int] = None

class UserAuthentification (BaseModel):
   
    UserId : Optional[int] 
    username : str
    password : str
    IP_address : Optional[str] = None
UserAuthentification.count = 0
class User(BaseModel):
    username : str
    password : str

@app.get("/",response_class=HTMLResponse,tags=["login"])
async def homepage(request:Request):
    return templats.TemplateResponse("Home.html",{"request":request})
    

#get
@app.get("/todo",tags=["todos"])
async def get_todo() ->dict:
    return {"data": todos}

#get post request below for user data
@app.get("/users/dataa",tags=["msg/prac"])
async def get_user_data():
    return {"user data" : user_data}
    #return{"data " :user_data }
# get book reviews data
@app.get("/users/get/books",tags=["msg/prac"])
def get_book_reviews():
    return {"books reviews": book_reviews}
  
@app.get("/user/get/messages",tags=["msg/prac"])
async def get_all_message_data():
    x = len(messages)
    return{"all messages being hosted on server currently": messages, "size" : x }



# post request
@app.post("/users/books",tags=["msg/prac"])
async def post_book_reviews(post_obj : post):
    id = post_obj.id 
    inner_list = []   # creates inner list for post object to store its information into
    inner_list.append(str(post_obj.title))
    inner_list.append(str(post_obj.content))
    messages.append(str(post_obj.content))   # this is just to add what ever content this is to the message list at the top of the code. we can use this data later if we want to store and see messages on the webstie
    inner_list.append(str(post_obj.publised))
    inner_list.append(str(post_obj.date_of_post))
    inner_list.append(str(post_obj.rating))
    #inner_list = inner_list + post_obj.content
    #results = post_obj.title + post_obj.content + post_obj.publised + post_obj.date_of_post + post_obj.rating
    #results = post_obj.title +" , " + post_obj.content + " , " + post_obj.str(published) + " , " + post_obj.str(date) + " , " + post_obj.str(rating)
    dict = {post_obj.id: inner_list} # after appending all post object data to a list we bind that list in a diction with the post id as the key 
    book_reviews.append(dict) # append the dictionary with the post id key and post values to book_reveiws list above. so that we can get information from said list and indexing it by using dictionary / json indexing
    if len(book_reviews) > 0:
        return {"data was posted succesfully": True }
    else:
        return{"data was posted succesfully":False, "post ": post_obj}





#post 
@app.post("/users/dataa",tags=["msg/prac"])
async def post_user_data(user : userModel):
    user_data.append(user.id)
    user_data.append(user.name)
    user_data.append(user.is_active)
    user_data.append(user.activities)

    return{"user id" : user.id , "user activs":user.activities}
#    user_dict = user.dict()
#    if user.id > 1:
#        x = today.strftime("%A, %dth of %B %Y")
 #       user.when_joined = x
 #   else:
  #      x = datetime.date.today()
 #       user.when_joined = x
 #  return {"data stored on website succesessfully, thanks": user.name,"data joined":user.when_joined}

    

#post
@app.post("/todo",tags=["todos"])
async def add_todo(todo:dict) -> dict:
    todos.append(todo)
    return{"data":"has been added succsessfully"}

#put request
# add the differencne in time from original creation of resource to the time that it is currently being resourced   time since last edit = orginal time of creation - current time of edit
# replace existing data with new data sent to api
@app.put("/todo/{id}",tags=["todos"])
def create_put_req(id:int , body:dict) -> dict:
    for todo in todos:
        if int((todo['id'])) == id:
            todo["activity"] = body["activity"]
            return {
                "data " : f"todo with id {id} has been replaced"
            }
    return{
        "data" : f"todo with this id number {id} was not found !"
    }


@app.delete('/todo/{id}',tags=["todos"])
async def delete_todos(id:int) -> dict:
    for todo in todos:
        if int((todo["id"])) == id:
            todos.remove(todo)
            return{
                "data" : f"todo with id {id} has been deleted"
            }
    return {
        "data": f"the todo with id {id} was not found"
    }



# works perfectly below
@app.post("/logg",response_model=UserAuthentification,tags=["login"])
async def create_user(request:Request,user_id: int = Form(...),
                      username: str = Form(...),
                      password: str = Form(...),
                      ip_address: str = Form(None)):
    # Create an instance of UserAuthentification with the form data
    user_data = UserAuthentification(UserId=UserAuthentification.count, username=username, password=password, IP_address=ip_address)
    # Increment the count of instances
    UserAuthentification.count += 1
    return user_data






@app.get("/log",tags=["login"])
async def log(request:Request):
    return templats.TemplateResponse("test.html",{"request": request})


class User(BaseModel):
    username : str
    password : str

@app.post("/loginpage/{user}",response_model=User)
async def submit(usn:str = Form(...),pwd:str = Form(...)):
    return User(username = usn,password=pwd)




# move to fucntion file later 
def isvalid(IP_address: str) -> bool:
    try:
        return True, ipaddress.ip_address(IP_address)
    except ValueError:
        print("what you entered was not a valid IP address")
        print(ValueError)
        return False


@app.get("/returnIP/",tags=["IP"])
async def return_client_IP(request : Request):
    client_ip = request.client.host
    if isvalid(client_ip)[0] == True:
        return {"ip" : client_ip}
    else:
        return "Server error. -richard wrote this. this  should never occur if this method is written properly"
    
#allows user to input there own ip address
#default ip address is the one attached to device. but they can alter it by assigning query parameters
@app.get("/returnIP/{ipaddress}",tags=["IP"])
async def return_client_IP(request : Request,ipaddress :Optional[str] = None):
   if isvalid(ipaddress)[0] == True:
       return "succsefully changed :)", {"ip":ipaddress}
   else:
       raise Exception
  
