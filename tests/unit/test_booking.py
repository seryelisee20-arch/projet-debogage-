import server


def test_prevent_booking_more_than_12_places_single_purchase(client):
    # She Lifts has 12 points, attempts to book 13 places
    response = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Winter Championship',
        'places': '13'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "ne pouvez pas réserver plus de 12 places".encode('utf-8') in response.data


def test_prevent_cumulative_booking_more_than_12_places(client):
    server.bookings_tracker.clear()
    # First booking: 8 places
    response1 = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Winter Championship',
        'places': '8'
    }, follow_redirects=True)
    assert response1.status_code == 200
    assert "réservation effectuée avec succès".encode('utf-8') in response1.data

    # Second booking: 5 places (8 + 5 = 13 > 12)
    response2 = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Winter Championship',
        'places': '5'
    }, follow_redirects=True)
    assert response2.status_code == 200
    assert "ne pouvez pas réserver plus de 12 places".encode('utf-8') in response2.data


def test_prevent_booking_more_than_competition_capacity(client):
    server.bookings_tracker.clear()
    comp = [c for c in server.competitions if c['name'] == 'Winter Championship'][0]
    initial_places = int(comp['numberOfPlaces'])
    comp['numberOfPlaces'] = '2'
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '3'
    }, follow_redirects=True)
    comp['numberOfPlaces'] = str(initial_places)
    assert response.status_code == 200
    assert "pas assez de places disponibles".encode('utf-8') in response.data


def test_prevent_booking_negative_places(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '-3'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "nombre de places positif".encode('utf-8') in response.data


def test_prevent_booking_zero_places(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '0'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "nombre de places positif".encode('utf-8') in response.data


def test_prevent_booking_non_integer_places(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': 'not_a_number'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Nombre de places demandé invalide".encode('utf-8') in response.data


def test_cannot_access_booking_for_full_competition(client):
    comp = [c for c in server.competitions if c['name'] == 'Winter Championship'][0]
    initial_places = comp['numberOfPlaces']
    comp['numberOfPlaces'] = '0'
    response = client.get('/book/Winter Championship/Simply Lift', follow_redirects=True)
    comp['numberOfPlaces'] = initial_places
    assert response.status_code == 200
    assert "Cette compétition est complète".encode('utf-8') in response.data


def test_cannot_purchase_places_for_full_competition(client):
    comp = [c for c in server.competitions if c['name'] == 'Winter Championship'][0]
    initial_places = comp['numberOfPlaces']
    comp['numberOfPlaces'] = '0'
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '2'
    }, follow_redirects=True)
    comp['numberOfPlaces'] = initial_places
    assert response.status_code == 200
    assert "Cette compétition est complète".encode('utf-8') in response.data
