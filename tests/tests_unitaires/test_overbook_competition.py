from Python_Testing import server
from Python_Testing.server import app


class TestPurchasePlaces:
    client = app.test_client()
    expected_status_code = 200

    
    def test_purchase_places_zero(self):
        club = server.clubs[1]
        comp = server.competitions[1]

        result = self.client.post(
            "/purchasePlaces",
            data={
                "competition": comp["name"],
                "club": club["name"],
                "places": 0,
            },
        )

        assert result.status_code == self.expected_status_code


    def test_purchase_places_over_12(self):
        club = server.clubs[0]
        comp = server.competitions[0]
        result = self.client.post("/purchasePlaces",
            data={
                "competition": comp["name"],
                "club": club["name"],
                "places": 13,
            },
        )
        assert result.status_code == self.expected_status_code


    def test_purchase_places_over_places_comp(self):
        club = server.clubs[0]
        competition = server.competitions[1]
        result = self.client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 27,
            },
        )
        assert result.status_code == self.expected_status_code


    def test_purchase_places_not_enought_club_points(self):
        competition = server.competitions[1]
        club = server.clubs[1]
        result = self.client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 5,
            },
        )
        assert result.status_code == self.expected_status_code


    def test_purchase_places_pts_club_nominal(self):
        competition = server.competitions[1]
        club = server.clubs[2]
        result = self.client.post(
            "/purchasePlaces",
            data={
                "competition": competition["name"],
                "club": club["name"],
                "places": 12,
                "points": 4,
            },
        )
        assert result.status_code == self.expected_status_code