from fastapi import FastAPI
from fastapi.testclient import TestClient

appPins = FastAPI()

@appPins.get("/pins/1")
async def read_main():
    return {"id":1,"title":"Toto au parc", "description": "c'est l\'histoire de toto au parc", "tag": "parc"}

pins = TestClient(appPins)

def test_read_main():
    response = pins.get("/")
    assert response.status_code == 200