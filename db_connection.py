import mysql.connector
 
db = mysql.connector.connect(
  host ="localhost",           
  user ="root",
  passwd ="root",
  database ="ConnectDB"
)

cursorObj = db.cursor()

cursorObj.execute("CREATE DATABASE IF NOT EXISTS ConnectDB") 

if db.is_connected():
    print("Connected to MySQL database")


def create_user(name, email, age):
    query = """insert into users (name,email,age) values (%s,%s,%s)"""
    val = (name, email, age)
    cursorObj.execute(query, val)
    db.commit()
    print(f"User {name} added sucessfully")
    

# create_user("John Doe", "john.doe@example.com", 24)


def read_user():
    query = "select * from users"
    cursorObj.execute(query)
    results = cursorObj.fetchall()
    for row in results:
        print(row)
        
# read_user()

def update_user(user_id,name=None,email=None,age=None):
    updates = []
    if name:
        updates.append(f"name='{name}'")
    if email:
        updates.append(f"email='{email}'")
    if age:
      updates.append(f"age={age}")
      
    if updates:
      updates_str = ", ".join(updates)
      query = f"update users set {updates_str} where id={user_id}"
      cursorObj.execute(query)
      db.commit()
      print(f"User with ID {user_id} updated sucessfully")
    

# update_user(5, name="Sanket", email="sanket@gmail.com", age=24)
read_user()
    

def delete_user(user_id):
    query = """delete from users where id = %s"""
    val = (user_id,)
    cursorObj.execute(query,val)
    db.commit()
    print(f"User with ID {user_id} deleted sucessfully")
    
# delete_user(8)