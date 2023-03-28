import pytest
from fastapi.testclient import TestClient
from .main import appPins, Pins

client = TestClient(appPins)

# Test de la route GET /pins
def test_get_pins():
    response = client.get('/pins')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de la route GET /pins/{pin_id}
def test_get_pin():
    response = client.get('/pins/1')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test de la route POST /pins
def test_create_pin():
    new_pin = Pins(title='Nouveau pin', description='Description du nouveau pin', tagNum=1)
    response = client.post('/pins', json=new_pin.dict())
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['title'] == new_pin.title

# Test de la route PUT /pins/{pin_id}
def test_update_pin():
    updated_pin = Pins(title='Pin mis à jour', description='Description du pin mise à jour', tagNum=2)
    response = client.put('/pins/1', json=updated_pin.dict())
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['title'] == updated_pin.title

# Test de la route DELETE /pins/{pin_id}
def test_delete_pin():
    response = client.delete('/pins/1')
    assert response.status_code == 200
    assert response.json()['message'] == 'Pin deleted'
