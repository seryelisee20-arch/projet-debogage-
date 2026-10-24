def test_public_points_reflect_after_booking(client):
    # Public board before booking
    res_before = client.get('/points')
    assert res_before.status_code == 200
    assert b"13 pts" in res_before.data  # Simply Lift has 13 points initially

    # Book 5 places for Simply Lift
    client.post('/purchasePlaces', data={
        'club': 'Simply Lift',
        'competition': 'Winter Championship',
        'places': '5'
    }, follow_redirects=True)

    # Public board after booking without login
    res_after = client.get('/points')
    assert res_after.status_code == 200
    assert b"8 pts" in res_after.data
