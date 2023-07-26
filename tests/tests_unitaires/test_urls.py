from Python_Testing.server import app


class TestUrlsPath:
    client = app.test_client()

    def test_url_show_board(self):
        result = self.client.get('/')
        assert result.status_code == 200

    def test_url_show_summary(self):
        result = self.client.get('/show-summary')
        assert result.status_code == 405

    def test_url_purchase_places(self):
        result = self.client.get('/purchase-places')
        assert result.status_code == 405

    def test_url_logout(self):
        result = self.client.get('/logout')
        assert result.status_code == 200

    def test_wrong_url_booking_club(self):
        result = self.client.get('/book/SpringFestival/Simply%20Lift')
        expected_result = 404
        assert result.status_code == expected_result

    def test_wrong_url_booking_competition(self):
        result = self.client.get('/book/Spring%20Festival/SimplyLift')
        expected_result = 404
        assert result.status_code == expected_result

    def test_incomplete_url(self):
        result = self.client.get('/book/Spring%20Festival')
        assert result.status_code == 404

    def test_wrong_url_root(self):
        result = self.client.get('/b00k/Spring%20Festival/Simply%20Lift')
        assert result.status_code == 404

    def test_good_url_booking(self):
        result = self.client.get('/book/Spring%20Festival/Simply%20Lift')
        assert result.status_code == 200