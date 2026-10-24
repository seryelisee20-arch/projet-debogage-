def test_points_deduction_on_successful_booking(client):
    # Simply Lift starts with 13 points, Winter Championship has places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '3'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Points disponibles : 10".encode('utf-8') in response.data


def test_prevent_booking_more_places_than_available_points(client):
    # Iron Temple has 4 points. Attempting to book 6 places should fail.
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Winter Championship',
        'places': '6'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "pas assez de points".encode('utf-8') in response.data
    assert "Points disponibles : 4".encode('utf-8') in response.data


def test_public_points_board_accessible_without_login(client):
    response = client.get('/points')
    assert response.status_code == 200
    assert "Points des Clubs".encode('utf-8') in response.data
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


def test_clubs_route_redirects_to_points(client):
    response = client.get('/clubs', follow_redirects=True)
    assert response.status_code == 200
    assert "Points des Clubs".encode('utf-8') in response.data
