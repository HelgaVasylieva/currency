
def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
