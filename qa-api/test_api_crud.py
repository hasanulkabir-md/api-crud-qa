import requests

BASE = "http://localhost:8000"

def test_create_user():
    data = {"name": "Kabir", "email": "kabir@example.com"}
    r = requests.post(f"{BASE}/users/", json=data)
    assert r.status_code == 200

def test_list_users():
    r = requests.get(f"{BASE}/users/")
    assert r.status_code == 200
    assert type(r.json()) == list

def test_get_user():
    r = requests.get(f"{BASE}/users/1")
    assert r.status_code in [200, 404]

def test_update_user():
    data = {"name": "NewName", "email": "new@example.com"}
    r = requests.put(f"{BASE}/users/1", json=data)
    assert r.status_code in [200, 404]

def test_delete_user():
    r = requests.delete(f"{BASE}/users/1")
    assert r.status_code in [200, 404]
