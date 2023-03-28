from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic import BaseModel
class Pins(BaseModel):
    id: int
    title: str
    description: str
    tagNum: int

appPins = FastAPI()

toTestPin = Pins(id=1, title="Toto au parc 1", description="c'est l\'histoire de toto au parc 1", tagNum=1)

@appPins.get("/pins")
async def read_main():
    return {"id":0,"title":"Toto au parc volume 2", "description": "c'est l\'histoire de toto au parc, volume 2", "tag": "1"}

pins = TestClient(appPins)

def test_read_main():
    response = pins.put("/pins/1", toTestPin)
    response = pins.post("/pins", json=toTestPin)
    assert response.status_code == 200



@appPins.put('/pins/{pin_id}', response_model=Pins)
def update_pin(pin_id: int, pin: Pins):
    return update_pin(pin_id, pin)

# Fonction pour mettre à jour un élément existant dans la base de données
def update_pin(pin_id, pin):
    c.execute('UPDATE pins SET title = ?, description = ?, fk_tags = ? WHERE id = ?', (pin.title, pin.description, pin.tagNum, pin_id))
    conn.commit()
    return {'id': pin_id, **pin.dict()}