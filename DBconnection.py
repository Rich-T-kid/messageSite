import mysql.connector
import json
from Models import *
db = mysql.connector.connect(host="localhost", 
                             user="root",
                             passwd="1019026",
                             database="messagesite")

mycursor = db.cursor(buffered=True)
sql_data = return_sql_data(45)

def return_table():
    mycursor.execute("select * from customers ")
    result = mycursor.fetchall()
    for row in result:
        print(row)

def check_for_Valid_primary_key() -> bool:
    # write method the that checks if that id value being inputed is valid or  if that value already exist in table 
    pass

def get_id(id):
    sqlFormula = "Select * from customers where id = %s"
    mycursor.execute(sqlFormula,(id,))
    result = mycursor.fetchone()
    for row in result:
        print(row)

def does_exist(column,valuetocheck):
    SqlFormula = f"select count(*) From customers where {column} ={valuetocheck}"
    mycursor.execute(SqlFormula)
    results = mycursor.fetchone()

    if results[0] > 0:
        return True
    else:
        return False

def insert_into_table_loop(items):
    for item in items:
        name =   item["name"] 
        address = str(item["address"]) 
        id  =  int(item["id"])

        sql_q = "INSERT INTO customers (name,address,id) VALUES (%s, %s, %s) "
        mycursor.execute(sql_q,(name,address,id))
        print("running")
def updatedlog(id,colum,new_data):
    sqlFormula = f"Select count(*) from customers where id = {id}"
    mycursor.execute(sqlFormula)
    result = mycursor.fetchone()
    if result[0] < 0:
        return "you cannot update a log that doesnt already exist in data base"
    else:
        sqlFormula1 = f"UPDATE customers set {colum} = {new_data} where id = {id}"
        mycursor.execute(sqlFormula1)
        db.commit()
        print("commited updates to db")
    pass

def add_values(name : str , address , idd,commit=False):
    if does_exist(id,idd):
        return "the Id column is unique yet your are trying to add duplicate Id values."
    else:
        sqlFormula = "INSERT INTO customers (name,address,id) values (%s,%s,%s)"
        mycursor.execute(sqlFormula,(name,address,idd))
        print("updated database")
        if commit == True:
            db.commit()
            print("updated database and commited changes")

def add_values_withoutid(name : str , address ,commit=False):
    sqlFormula = "INSERT INTO customers (name,address) values (%s,%s)"
    mycursor.execute(sqlFormula,(name,address))
    print("updated database")
    if commit == True:
        db.commit()
        print("updated database and commited changes")

def return_col_names():
    sqlFormulas = " show columns from customers;"
    mycursor.execute(sqlFormulas)
    pass

def return_certain_rows(row,return_1=True):
    sqlFormula = "Select {row} from customers"
    mycursor.execute(sqlFormula)
    if return_1 == True:
        results = mycursor.fetchone()
        for i in results:
            return i
    else:
        results = mycursor.fetchall()
        for i in results:
            return i
#returns certain rows based on inputed contion
def return_certain_rows_q(row,condtion: str ):
    sqlFormula = f"Select {row} from customers  where {condtion}"
    mycursor.execute(sqlFormula)
    results = mycursor.fetchall()
    for i in results:
        return i

#code below is not completed. figure out why no values are being outputed
def over_xchar(colum,id):
    sqlFormula = f"select Char_length({colum}) from customers where id = {id}"
    mycursor.execute(sqlFormula)
    results = mycursor.fetchone()
    # only typcasting to int because we cant compare an int with a tuple note placing values inside parthesis with a comma makes them a tuple even if its the only value inside 
    """x = tuple(1)
    print(type(x))"""
    print(type(results))
    print(type(1))
    print(results[0])
    if len(results) < 1:
        return "error has occured that column returned a value less than one"
    else:
        return f"length of your colum is {results}"
    pass

#add method that retuns what ever query supplied but also limits the amount of content returned Hint: LIMIT X

# add a method that orders the returned results. this will also have two options. limit the number of returns and allow what column to order the data by Hint: ORDERBY ASC DES
# wait to use
"""
insert_into_table_loop(sql_data)
return_table()
db.commit()"""
#add_values("richard_the_flamelord","223 newyorkwashignton ave")

over_xchar("address",8)

# similar syntax when finding hashes and salts in db
"""SELECT column1, column2, ... 
FROM table_name 
WHERE column_name = 'exact_value';"""