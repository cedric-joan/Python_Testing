from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def clubs_table(self):
        self.client.get("/clubs")

    @task
    def show_summary(self):
        self.client.post("/show-summary", {"email": "john@simplylift.co"})

    @task
    def booking(self):
        self.client.get("/book/New Games/Simply Lift")

    @task
    def purchase_place(self):
        self.client.post("/purchase-places", {"club": "Simply Lift", "competition": "New Games", "places": 4})

    @task
    def logout(self):
        self.client.get("/logout")