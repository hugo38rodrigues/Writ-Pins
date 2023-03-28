from fastapi.testclient import TestClient
from main import appPins, Pins

client = TestClient(appPins)

def test_create_pin():
    # Envoie une requête POST avec un nouvel élément
    response = client.post("/pins", json={"title": "Nouveau pin", "description": "Description du nouveau pin", "tagNum": 1})
    assert response.status_code == 200
    assert response.json()["title"] == "Nouveau pin"
    assert response.json()["description"] == "Description du nouveau pin"
    assert response.json()["tagNum"] == 1

def test_get_all_pins():
    # Envoie une requête GET pour récupérer tous les éléments
    response = client.get("/pins")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_pin_by_id():
    # Crée un nouvel élément et récupère son ID
    new_pin = client.post("/pins", json={"title": "Nouveau pin", "description": "Description du nouveau pin", "tagNum": 1})
    new_pin_id = new_pin.json()["id"]
    # Envoie une requête GET pour récupérer l'élément par ID
    response = client.get(f"/pins/{new_pin_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Nouveau pin"
    assert response.json()["description"] == "Description du nouveau pin"
    assert response.json()["tagNum"] == 1

def test_update_pin():
    # Crée un nouvel élément et récupère son ID
    new_pin = client.post("/pins", json={"title": "Nouveau pin", "description": "Description du nouveau pin", "tagNum": 1})
    new_pin_id = new_pin.json()["id"]
    # Envoie une requête PUT pour mettre à jour l'élément
    response = client.put(f"/pins/{new_pin_id}", json={"title": "Pin mis à jour", "description": "Description du pin mise à jour", "tagNum": 2})
    assert response.status_code == 200
    assert response.json()["title"] == "Pin mis à jour"
    assert response.json()["description"] == "Description du pin mise à jour"
    assert response.json()["tagNum"] == 2

def test_delete_pin():
    # Crée un nouvel élément et récupère son ID
    new_pin = client.post("/pins", json={"title": "Nouveau pin", "description": "Description du nouveau pin", "tagNum": 1})
    new_pin_id = new_pin.json()["id"]
    # Envoie une requête DELETE pour supprimer l'élément
    response = client.delete(f"/pins/{new_pin_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Pin deleted"
