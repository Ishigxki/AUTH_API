from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt
from database import connection, cursor

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    try:
        hashed_password = bcrypt.hashpw(
            user.password.encode('utf-8'),
            bcrypt.gensalt()
        )
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);",
            (user.username, hashed_password.decode('utf-8'))
        )
        connection.commit()
        return {"message": "User registered"}
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/login")
def login(user: User):

    try:
        cursor.execute(
        "SELECT password FROM users WHERE username = %s;",
        (user.username,)
        )

        result = cursor.fetchone()

        if result is None:
             return {"error": "User not found"}
            
        stored_password = result[0]

        if bcrypt.checkpw(
                user.password.encode('utf-8'),
                stored_password.encode('utf-8')
            ):
                
                return {"message": "Login successful"}
        
        return {"error": "Invalid credentials"}
    
    except Exception as e:
        return {"error": str(e)}