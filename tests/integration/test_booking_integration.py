def test_full_booking_workflow(client):
    # 1. Access login page
    home = client.get('/')
    assert home.status_code == 200

    # 2. Login as secretary
    login = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'}, follow_redirects=True)
    assert login.status_code == 200
    assert "Bienvenue, kate@shelifts.co.uk".encode('utf-8') in login.data
    assert "Points disponibles : 12".encode('utf-8') in login.data

    # 3. Access booking page for future competition
    booking_page = client.get('/book/Winter Championship/She Lifts')
    assert booking_page.status_code == 200
    assert "Réservation pour She Lifts".encode('utf-8') in booking_page.data

    # 4. Purchase 4 places
    purchase = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Winter Championship',
        'places': '4'
    }, follow_redirects=True)
    assert purchase.status_code == 200
    assert "réservation effectuée avec succès".encode('utf-8') in purchase.data
    assert "Points disponibles : 8".encode('utf-8') in purchase.data

    # 5. Logout
    logout = client.get('/logout', follow_redirects=True)
    assert logout.status_code == 200
    assert "Bienvenue sur le portail d'inscription GUDLFT".encode('utf-8') in logout.data
