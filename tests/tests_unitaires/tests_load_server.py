from Python_Testing import server


# class TestLoadClubs:
def test_load_clubs_data():
    clubs_json = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    expected_result = clubs_json
    result = server.loadClubs()
    assert result == expected_result


# class TestLoadCompetitions:
def test_load_competitions_nominal():
    competitions_json = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]
    expected_result = competitions_json
    result = server.loadCompetitions()
    assert result == expected_result