from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Définition des modèles de données pour les utilisateurs et les épingles
class User(BaseModel):
    firstname: str
    name: str
    birthday: date
    email: str
    password: str


class Pin(BaseModel):
    title: str
    description: str
    status: bool
    tags: str


# Connexion à la base de données SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS pins
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEST NOT NULL,
            status BOOLEAN NOT NULL,
            tag_name INTEGER NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             firstname TEXT NOT NULL,
            name TEXT NOT NULL,
            birthday Date NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL)''')
conn.commit()


# Définition des fonctions pour les opérations CRUD sur les utilisateurs et les épingles

# Fonctions pour les utilisateurs
@app.post("/v0/post/users")
def create_user(user: User):
    try:
        cursor.execute('INSERT INTO users (firstname, name, email, password, birthday) VALUES (?, ?, ?)',
                       (user.username, user.email, user.password))
        conn.commit()
        return {"message": "User created successfully!"}
    except:
        raise HTTPException(status_code=400, detail="Error creating user")


@app.get("/v0/get/users")
def read_user(user_id: int):
    cursor.execute('SELECT * FROM users')
    user = cursor.fetchone()
    if user:
        return {"id": user[0], "username": user[1], "email": user[2]}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/v0/put/put/users/{user_id}")
def update_user(user_id: int, user: User):
    try:
        cursor.execute('UPDATE users SET firstname=?, name=?, email=?, password=?, birthday=? WHERE id=?',
                       (user.username, user.email, user.password, user_id))
        conn.commit()
        return {"message": "User updated successfully!"}
    except:
        raise HTTPException(status_code=400, detail="Error updating user")


@app.delete("/v0/delete/users/{user_id}")
def delete_user(user_id: int):
    try:
        cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
        conn.commit()
        return {"message": "User deleted successfully!"}
    except:
        raise HTTPException(status_code=400, detail="Error deleting user")


# Fonctions pour les épingles (pins)
@app.post("/v0/post/pins")
def create_pin(pin: Pin):
    try:
        cursor.execute('INSERT INTO pins (title, description, status, tags) VALUES (?, ?)',
                       (pin.title, pin.description, pin.status, pin.tags))
        conn.commit()
        return {"message": "Pin created successfully!"}
    except:
        raise HTTPException(status_code=400, detail="Error creating pin")


@app.get("/v0/get/pins")
def read_pin(pin_id: int):
    cursor.execute('SELECT * FROM pins')
    pin = cursor.fetchone()
    if pin:
        return {"id": pin[0], "title": pin[1], "description": pin[2], "status": pin[3], "tags": pin[4]}
    else:
        raise HTTPException(status_code=404, detail="Pin not found")


@app.put("/v0/put/pins/{pin_id}")
def update_pin(pin_id: int, pin: Pin):
    try:
        cursor.execute('UPDATE pins SET title=?, description=?, status=?, tags=? WHERE id=?',
                       (pin.title, pin.description, pin.status, pin.tags, pin_id))
        conn.commit()
        return {"message": "Pin updated successfully!"}
    except:
        raise HTTPException(status_code=400, detail="Error updating pin")


@app.delete("/v0/delete/pins/{pin_id}")
def delete_pin(pin_id: int):
    try:
        cursor.execute('DELETE FROM pins WHERE id=?', (pin_id,))
        conn.commit()
        return {"message": "Pin deleted successfully!"}
    except:
        raise HTTPException(status_code=400, detail="Error deleting user")
