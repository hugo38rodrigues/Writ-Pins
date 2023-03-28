from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Middleware CORS pour permettre les requêtes HTTP depuis n'importe quel domaine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Création d'une classe modèle pour les données de l'objet
class Item(BaseModel):
    name: str
    price: float

# Configuration de la base de données SQLite
conn = sqlite3.connect('items.db')
c = conn.cursor()

# Création de la table "items" si elle n'existe pas déjà
c.execute('''CREATE TABLE IF NOT EXISTS items
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              price REAL NOT NULL)''')
conn.commit()

# Fonction pour récupérer tous les éléments de la base de données
def get_all_items():
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    return [{'id': item[0], 'name': item[1], 'price': item[2]} for item in items]

# Fonction pour récupérer un élément spécifique de la base de données par ID
def get_item_by_id(item_id):
    c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = c.fetchone()
    if item:
        return {'id': item[0], 'name': item[1], 'price': item[2]}
    else:
        raise HTTPException(status_code=404, detail='Item not found')

# Fonction pour ajouter un élément à la base de données
def add_item(item):
    c.execute('INSERT INTO items (name, price) VALUES (?, ?)', (item.name, item.price))
    conn.commit()
    return {'id': c.lastrowid, **item.dict()}

# Fonction pour mettre à jour un élément existant dans la base de données
def update_item(item_id, item):
    c.execute('UPDATE items SET name = ?, price = ? WHERE id = ?', (item.name, item.price, item_id))
    conn.commit()
    return {'id': item_id, **item.dict()}

# Fonction pour supprimer un élément de la base de données par ID
def delete_item(item_id):
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    return {'message': 'Item deleted'}

# Définition des routes de l'API
@app.get('/items', response_model=List[Item])
def get_items():
    return get_all_items()

@app.get('/items/{item_id}', response_model=Item)
def get_item(item_id: int):
    return get_item_by_id(item_id)

@app.post('/items', response_model=Item)
def create_item(item: Item):
    return add_item(item)

@app.put('/items/{item_id}', response_model=Item)
def update_item(item_id: int, item: Item):
    return update_item(item_id, item)

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    return delete_item(item_id)
