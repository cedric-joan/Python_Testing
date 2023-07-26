import pytest
from Python_Testing.server import app, init_club_bookings

app.config['TESTING'] = True


@pytest.fixture
def clubs():
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
    return clubs


@pytest.fixture
def competitions():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
    return competitions


@pytest.fixture
def client(mocker, clubs, competitions):
    mocker.patch.object(app, "clubs", clubs)
    mocker.patch.object(app, "competitions", competitions)
    bookings = init_club_bookings(clubs, competitions)
    mocker.patch.object(app, "bookings", bookings)
    with app.test_client() as client:
        yield client