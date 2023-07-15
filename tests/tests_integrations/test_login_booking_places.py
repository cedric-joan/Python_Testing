from Python_Testing.server import app

client = app.test_client()

def test_login_route(clubs, competitions):
    result = client.get("/")
    assert result.status_code == 200
    assert b"email" in result.data

    result = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert result.status_code == 200
    assert b'Welcome, admin@irontemple.com' in result.data

    result = client.get('/book/Spring%20Festival/Iron%20Temple')
    assert result.status_code == 200
    assert b'How many places?' in result.data

    result = client.post('/purchasePlaces', 
                        data={'competition': 'Spring Festival',
                        'club': 'Iron Temple', 
                        'places': 4}, follow_redirects=True)
    assert result.status_code == 200
    assert b'Great-booking complete!' in result.data
    result = int(competitions[0]['numberOfPlaces']) - int(clubs[1]['points'])
    expected_value = 21
    assert clubs[1]['name'] == "Iron Temple"
    assert  result == expected_value

    result = client.get('/logout', data={'email': 'admin@irontemple.com'})
    assert result.status_code == 200