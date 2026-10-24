def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal" in response.data


def test_login_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_login_unknown_email(client):
    response = client.post('/showSummary', data={'email': 'unknown@club.com'}, follow_redirects=True)
    assert response.status_code in (200, 401)
    assert b"Sorry, that email was not found." in response.data


def test_login_empty_email(client):
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=True)
    assert response.status_code in (200, 401)
    assert b"Sorry, that email was not found." in response.data
