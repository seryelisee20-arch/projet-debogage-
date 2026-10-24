def test_points_deduction_on_successful_booking(client):
    # Simply Lift starts with 13 points, Winter Championship has places
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '3'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Points available: 10" in response.data


def test_prevent_booking_more_places_than_available_points(client):
    # Iron Temple has 4 points. Attempting to book 6 places should fail.
    response = client.post('/purchasePlaces', data={
        'club': 'Iron Temple',
        'competition': 'Winter Championship',
        'places': '6'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"You do not have enough points" in response.data
    assert b"Points available: 4" in response.data


def test_public_points_board_accessible_without_login(client):
    response = client.get('/points')
    assert response.status_code == 200
    assert b"Clubs Points Summary" in response.data
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


def test_clubs_route_redirects_to_points(client):
    response = client.get('/clubs', follow_redirects=True)
    assert response.status_code == 200
    assert b"Clubs Points Summary" in response.data
