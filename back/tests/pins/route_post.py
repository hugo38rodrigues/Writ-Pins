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
    assert response.status_code == 200