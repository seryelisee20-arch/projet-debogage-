from locust import HttpUser, task, between


class GudlftSecretaryUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def view_home(self):
        """Test home page load (threshold < 5s)"""
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5.0:
                response.failure("Home page took longer than 5 seconds to load")
            else:
                response.success()

    @task(3)
    def view_public_points_board(self):
        """Test public points board page (threshold < 5s)"""
        with self.client.get("/points", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5.0:
                response.failure("Points board took longer than 5 seconds to load")
            else:
                response.success()

    @task(2)
    def secretary_login(self):
        """Test login and competitions retrieval (threshold < 5s)"""
        with self.client.post("/showSummary", data={"email": "john@simplylift.co"}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 5.0:
                response.failure("Competitions retrieval took longer than 5 seconds")
            else:
                response.success()

    @task(2)
    def view_booking_page(self):
        """Test booking page display (threshold < 5s)"""
        with self.client.get("/book/Winter Championship/Simply Lift", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5.0:
                response.failure("Booking page took longer than 5 seconds to load")
            else:
                response.success()

    @task(1)
    def update_points_purchase(self):
        """Test points update via purchasePlaces (threshold < 2s)"""
        with self.client.post("/purchasePlaces", data={
            "club": "Simply Lift",
            "competition": "Winter Championship",
            "places": "1"
        }, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2.0:
                response.failure("Points update took longer than 2 seconds")
            else:
                response.success()
