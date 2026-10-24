import server


def test_cannot_access_booking_page_for_past_competition(client):
    response = client.get('/book/Spring Festival/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot book places for past competitions" in response.data


def test_cannot_purchase_places_for_past_competition(client):
    response = client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Spring Festival',
        'places': '2'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot book places for past competitions" in response.data


def test_can_access_booking_page_for_future_competition(client):
    response = client.get('/book/Winter Championship/Simply Lift')
    assert response.status_code == 200
    assert b"Winter Championship" in response.data
    assert b"Places available: 20" in response.data


def test_is_competition_past_invalid_date_format():
    assert server.is_competition_past("invalid-date-format") is False
    assert server.is_competition_past(None) is False
