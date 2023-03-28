from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    password: str
    email: str
    birthdate: date

db = []

@app.post("/users/")
def create_user(user: User):
    db.append(user)
    return user

@app.get("/users/{user_id}")
def read_user(user_id: int):
    for user in db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for index, user_db in enumerate(db):
        if user_db.id == user_id:
            db[index] = user
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(db):
        if user.id == user_id:
            db.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
