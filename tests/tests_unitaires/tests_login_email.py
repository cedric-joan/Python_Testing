from Python_Testing.server import app

client = app.test_client()

def test_is_empty_email():
    result = client.post('/showSummary', data={'email': ''})
    assert result.status_code == 401

def test_invalid_email():
    result = client.post('/showSummary', data={'email': 'john.doe@graveyard.com'})
    assert result.status_code == 401

def test_is_valid_email():
    result = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert result.status_code == 200
