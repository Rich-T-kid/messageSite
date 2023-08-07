from fastapi import FastAPI ,Form , Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, Response,HTMLResponse
from typing import Any, ClassVar
from fastapi.staticfiles import StaticFiles
from Models import Identifyer,Address
from impo_meth  import generate_password_salt , randompassword ,createRandomPassword , Hash_salt_andpassword , check_password , validLogin , return_userlocationbasedoffIP,is_ip_private
from datetime import date
from typing import Optional
from pydantic import BaseModel , Field
import ipaddress
from datetime import datetime
import requests
import time

User_name_andpword = []
salt_and_Hashdb = []
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
    UserId : Optional[int] = None
    UserName : str
    Password : str
    IP_Adress : Optional[str] = None
   
class MessagesClass(BaseModel):
    Sender_id : Optional[int] = None
    Message_ : str
    date_Sent : str
    textsize : int
    Recept_id : Optional[int] = None
    

UserAuthentification.count = 0 

class LoginModel(BaseModel):
    userdata : UserAuthentification
    login_id : int
class User(BaseModel):
    username : str
    password : str
# middleware logs the time it took to finish proccesing a request
@app.middleware("http")
async def add_proccessTime(request:Request,call_next):
    start_time = time.time()
    Response = await call_next(request)
    proccess_Time = time.time() - start_time
    Response.headers["X-Proccess-Time"] = str(proccess_Time)
    return Response

@app.middleware("http")
async def print_consol(request:Request,call_next):
    print(f"recived request: {request.method} {request.url}")
    response = await call_next(request)
    return response
#set defualt headers for website
@app.middleware("http")
async def print_post(request:Request,call_next):
    if request.method == "GET" or "POST" or "PUT" or "DELETE":
        response = await call_next(request)
        client_Ip = request.client.host
        user_Origin_location= return_userlocationbasedoffIP(client_Ip)
        pubVpriv = is_ip_private(client_Ip)
        response.headers["X-Request-Type"] = request.method
        response.headers["User-IP-Address"] = client_Ip
        response.headers["Content-Language"] = "ENG"
        if str(user_Origin_location) == "None":
             response.headers["X-IP-Type"] = str(pubVpriv)
             response.headers["User-origin-country"] = "your on local server it wont LOL."
        else:
            response.headers["User-origin-country"] = str(user_Origin_location)
            response.headers["X-IP-Type"]  = str(pubVpriv)
        return response
    return await call_next(request)

# keep count of get request of page visist to the home page
count = 0
@app.middleware("http")
async def add_count_home(request:Request,call_next):
    if request.method == "GET" and request.url.path == "/":
        response = await call_next(request)
        global count 
        count += 1
        print("somone has entered home page")
        print("added to count")
        return response 
    return await call_next(request)
@app.middleware("http")
async def print_post(request:Request,call_next):
    if request.method == "POST":
        response = await call_next(request)
        response.headers["X-Request-Type"] ="Post Request"
        print("incoming Post Request")
        return response
    return await call_next(request)

@app.get("/",response_class=HTMLResponse,tags=["login"])
async def homepage(request:Request):
    return templats.TemplateResponse("Home.html",{"request":request})
    
@app.post("/",tags=["login"])
async def Login_data(request:Request,usid:int = Form(None),ussername : str = Form(...),pasw:str = Form(...)): # store data into forms
    new_user = UserAuthentification(UserId=usid,UserName=ussername,Password=pasw) # store all that form data into an objec
    #implement login logic here for example  checking length of strings 
    # store the username and password 
    if validLogin(username=new_user.UserName,password=new_user.Password) == True:
        x = {UserAuthentification.count:new_user}
        User_name_andpword.append(x) # add dictionary to main database in this case just a list
        salt = generate_password_salt()
        hashedpassword =Hash_salt_andpassword(salt=salt,password=new_user.Password)
        salt_and_Hashdb.append({UserAuthentification.count:{"salt":salt,"hashed-password+salt":hashedpassword}})
        UserAuthentification.count +=  1
        return templats.TemplateResponse("Homepage.html",{"request":request})
    else:
        return templats.TemplateResponse("extra.html",{"request":request})

@app.get("/Homepage",tags=["login"])
async def returnHomepage(request:Request):
    return templats.TemplateResponse("Homepage.html",{"request":request})

@app.get("/all",tags=["login"])
async def returnpasswords():
    return salt_and_Hashdb


@app.get("/json/{user}",tags=["login"])
async def login_data(user: int):
    if user < len(User_name_andpword):
        return User_name_andpword[user]
    else:
        return {"message": "User not found"}
    
@app.get("/allusers/json",tags=["login"])
async def AllLoginData():
    all_objects = len(User_name_andpword)
    return User_name_andpword,{"amount of objects": all_objects}
class User(BaseModel):
    username : str
    password : str

@app.post("/loginpage/{user}",response_model=User,tags=["login"])
async def submit(usn:str = Form(...),pwd:str = Form(...)):
    return User(username = usn,password=pwd)
#MessagesL = [{1:[1, 'hello this is a message', '2023-09-09 12:32:15', 65, None]}, ]
MessagesL = {}
message_count = 0

@app.get("/MessagesMain",tags=["Messages"])
async def Return_MessageHtml(request:Request):
    return templats.TemplateResponse("Message.html",{"request":request})

@app.post("/MessagesMain",tags=["Messages"])
async def Send_message(request:Request,sendID:int = Form(...),
                       Message_ : str =Form(...),
                       date_Sent:str=Form(None),
                       textsize:int=Form(None),
                       Recept_id:int=Form()):
    global message_count 
    current_time = datetime.now()
    realuse = current_time.strftime("%Y-%m-%d %H:%M:%S")
    tempvarsize = len(Message_)
    NewMSg = MessagesClass(Sender_id=sendID,
                           Message_=Message_,
                           date_Sent=realuse,
                           textsize=tempvarsize,
                           Recept_id=Recept_id)
    
    if NewMSg.Sender_id in MessagesL:
        MessagesL[NewMSg.Sender_id].append(NewMSg)
    else:
        MessagesL[NewMSg.Sender_id] = [NewMSg]
    message_count += 1

    return NewMSg
    #return templats.TemplateResponse("temp.html",{"request":request})
"""if tempvarsize > 5 :
        New_Message = Messages(sendID=UserAuthentification.count,Message_=Message_,date_Sent=realuse,textsize=tempvarsize,Recept_id=None)
       """

@app.get("/allmessages",tags=["Messages"])
async def getallmessage():
    return MessagesL

@app.get('/MsgSentby/{UserId}',tags=["Messages"])
async def findAllmessages(UserId: int):
    return MessagesL[UserId]
@app.get("/message/keys",tags=["Messages"])
async def NeverUseagain():
    return MessagesL.keys()



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
"""@app.post("/logg",response_model=UserAuthentification,tags=["login"])
async def create_user(request:Request,user_id: int = Form(...),
                      username: str = Form(...),
                      password: str = Form(...),
                      ip_address: str = Form(None)):
    # Create an instance of UserAuthentification with the form data
    user_data = UserAuthentification(UserId=UserAuthentification.count, username=username, password=password, IP_address=ip_address)
    # Increment the count of instances
    UserAuthentification.count += 1
    return user_data

"""




@app.get("/log",tags=["login/2"])
async def alternate_login_page(request:Request):
    return templats.TemplateResponse("test.html",{"request": request})




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
       return "succsefully changed :)", {"ip":ipaddress},
   else:
       raise Exception

@app.get("/numberofvisits")
async def returnnubmerofvisst():
    return {"Visits since server started ": count}