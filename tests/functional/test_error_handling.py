def test_invalid_competition_or_club_in_booking_url(client):
    # Non-existent competition
    response = client.get('/book/NonExistentCompetition/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert "Une erreur est survenue".encode('utf-8') in response.data

    # Non-existent club
    response = client.get('/book/Winter Championship/NonExistentClub', follow_redirects=True)
    assert response.status_code == 200
    assert "Une erreur est survenue".encode('utf-8') in response.data
