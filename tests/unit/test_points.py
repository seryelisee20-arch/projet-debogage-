def test_points_deduction_on_successful_booking(client):
    # She Lifts starts with 12 points, Spring Festival starts with places
    # Let's test booking 3 places
    response = client.post('/purchasePlaces', data={
        'club': 'She Lifts',
        'competition': 'Spring Festival',
        'places': '3'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Points available: 9" in response.data
