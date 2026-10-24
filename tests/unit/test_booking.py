import server


def test_prevent_booking_more_than_12_places_single_purchase(client):
    # She Lifts has 12 points, attempts to book 13 places
    response = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Spring Festival',
        'places': '13'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"cannot book more than 12 places" in response.data


def test_prevent_cumulative_booking_more_than_12_places(client):
    server.bookings_tracker.clear()
    # First booking: 8 places
    response1 = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Spring Festival',
        'places': '8'
    }, follow_redirects=True)
    assert response1.status_code == 200
    assert b"Great-booking complete!" in response1.data

    # Second booking: 5 places (8 + 5 = 13 > 12)
    response2 = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Spring Festival',
        'places': '5'
    }, follow_redirects=True)
    assert response2.status_code == 200
    assert b"cannot book more than 12 places" in response2.data
