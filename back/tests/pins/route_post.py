from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic import BaseModel
class Pins(BaseModel):
    id: int
    title: str
    description: str
    tagNum: int

appPins = FastAPI()

toTestPin = Pins(id=0, title="Toto au parc, volume 2", description="c'est l\'histoire de toto au parc, volume 2", tagNum=1)

@appPins.post("/pins")
async def read_main():
    return {"id":2,"title":"Toto au parc volume 2", "description": "c'est l\'histoire de toto au parc, volume 2", "tag": "1"}

pins = TestClient(appPins)

def test_read_main():
    response = pins.post("/pins", json=toTestPin)
    print(response)
    assert response.status_code == 200
    





@appPins.post('/pins', response_model=Pins)
def create_item(pin: Pins):
    return add_pin(pin)

# Fonction pour ajouter un élément à la base de données
def add_pin(pin):
    c.execute('INSERT INTO pins (title, description, fk_tags) VALUES (?, ?)', (pin.title, pin.description, pin.tagNum))
    conn.commit()
    return {'id': c.lastrowid, **pin.dict()}
