import pytest
from backend import create_app


@pytest.fixture(name='client')
def create_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as current_client:
        yield current_client


def test_get_animals(client):
    response = client.get('/api/animals')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_get_animal_not_found(client):
    response = client.get('/api/animals/unknown')
    assert response.status_code == 404


def test_add_animal_success(client):
    new_animal = {"name": "Tiger",
                  "species": "Panthera tigris", "habitat": "Forest"}
    response = client.post('/api/animals', json=new_animal)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Tiger"


def test_add_animal_missing_field(client):
    incomplete_animal = {"name": "Giraffe",
                         "species": "Giraffa camelopardalis"}
    response = client.post('/api/animals', json=incomplete_animal)
    assert response.status_code == 400

def test_get_animals_can_filter_by_habitat(client):
    response = client.get('/api/animals?habitat=savannah')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert all(animal["habitat"] == "Savannah" for animal in data)


def test_get_animals_returns_empty_list_for_unknown_habitat(client):
    response = client.get('/api/animals?habitat=Ocean')

    assert response.status_code == 200
    assert response.get_json() == []
