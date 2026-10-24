def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Bienvenue sur le portail d'inscription GUDLFT".encode('utf-8') in response.data


def test_login_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert response.status_code == 200
    assert "Bienvenue, john@simplylift.co".encode('utf-8') in response.data


def test_login_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@club.com'}, follow_redirects=True)
    assert response.status_code in (200, 401)
    assert "cette adresse email est introuvable".encode('utf-8') in response.data


def test_login_empty_email(client):
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code in (200, 401)
    assert "cette adresse email est introuvable".encode('utf-8') in response.data
