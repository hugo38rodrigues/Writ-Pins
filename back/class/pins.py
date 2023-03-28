from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

appPins = FastAPI()

# Middleware CORS pour permettre les requêtes HTTP depuis n'importe quel domaine
appPins.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Création d'une classe modèle pour les données de l'objet
class Pins(BaseModel):
    id: int
    title: str
    description: str
    tagNum: int

# Configuration de la base de données SQLite
conn = sqlite3.connect('pins.db')
c = conn.cursor()


# TODO: Modifier pour rajouter une liaison
# Création de la table "pins" et "tags" si elle n'existe pas déjà
c.execute('''CREATE TABLE IF NOT EXISTS tags
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT NOT NULL)''')
c.execute('''CREATE TABLE IF NOT EXISTS pins
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEST NOT NULL,
            fk_tags INTEGER NOT NULL)''')
c.execute('''ALTER TABLE pins ADD FOREIGN KEY (fk_item) REFERENCES tags(id)''')
conn.commit()


# Fonction pour récupérer tous les éléments de la base de données
def get_all_pins():
    c.execute('SELECT * FROM pins INNER JOIN tags ON pins.fk_tags = tags.id')
    pins = c.fetchall()
    return [{'id': pin[0], 'title': pin[1], 'description': pin[2], 'tag_name': pin[3]} for pin in pins]

# Fonction pour récupérer un élément spécifique de la base de données par ID
def get_pin_by_id(pin_item):
    c.execute('SELECT * FROM pins INNER JOIN tags ON pins.fk_tags = tags.id WHERE id = ?', (pin_item,))
    pin = c.fetchone()
    if pin:
        return {'id': pin[0], 'title': pin[1], 'description': pin[2], 'tag_name': pin[3]}
    else:
        raise HTTPException(status_code=404, detail='Pin not found')

# Fonction pour ajouter un élément à la base de données
def add_pin(pin):
    c.execute('INSERT INTO pins (title, description, fk_tags) VALUES (?, ?)', (pin.title, pin.description, pin.tagNum))
    conn.commit()
    return {'id': c.lastrowid, **pin.dict()}

# Fonction pour mettre à jour un élément existant dans la base de données
def update_pin(pin_id, pin):
    c.execute('UPDATE pins SET title = ?, description = ?, fk_tags = ? WHERE id = ?', (pin.title, pin.description, pin.tagNum, pin_id))
    conn.commit()
    return {'id': pin_id, **pin.dict()}

# Fonction pour supprimer un élément de la base de données par ID
def delete_pin(pin_id):
    c.execute('DELETE FROM pins WHERE id = ?', (pin_id,))
    conn.commit()
    return {'message': 'Pin deleted'}

# Définition des routes de l'API
@appPins.get('/pins', response_model=List[Pins])
def get_pins():
    return get_all_pins()

@appPins.get('/pins/{pins_id}', response_model=Pins)
def get_pin(pin_id: int):
    return get_pin_by_id(pin_id)

@appPins.post('/pins', response_model=Pins)
def create_item(pin: Pins):
    return add_pin(pin)

@appPins.put('/pins/{pin_id}', response_model=Pins)
def update_pin(pin_id: int, pin: Pins):
    return update_pin(pin_id, pin)

@appPins.delete('/pins/{pin_id}')
def delete_pin(pin_id: int):
    return delete_pin(pin_id)
