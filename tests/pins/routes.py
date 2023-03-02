from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/pins")
async def read_main():
    return {"id":1,"title":"Toto au parc", "description": "c'est l\'histoire de toto au parc", "tag":['tag1',"tag2","tag3"]}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}