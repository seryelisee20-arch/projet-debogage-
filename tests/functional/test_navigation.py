def test_full_user_navigation(client):
    # Visitor arrives at landing page
    response = client.get('/')
    assert response.status_code == 200
    assert "Bienvenue sur le portail d'inscription GUDLFT".encode('utf-8') in response.data

    # Visitor browses the public points board
    response = client.get('/points')
    assert response.status_code == 200
    assert "Points des Clubs".encode('utf-8') in response.data

    # Visitor returns to login page
    response = client.get('/')
    assert response.status_code == 200

    # Visitor logs in with valid credentials
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert response.status_code == 200
    assert "Bienvenue, john@simplylift.co".encode('utf-8') in response.data

    # User clicks logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert "Bienvenue sur le portail d'inscription GUDLFT".encode('utf-8') in response.data
