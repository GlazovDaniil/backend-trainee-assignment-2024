from locust import HttpUser, task, between
from random import randint


class LoadTestUser(HttpUser):

    def on_start(self) -> None:
        token = 'a83434fe4f784129cad0dfd111cbaf4614b162d3'
        self.client.headers["Authorization"] = f"Token {token}"

    @task
    def load_test_endpoint(self):
        a = randint(1, 3)
        b = randint(1, 3)
        self.client.get(f'/user_banner/?tag_id=1&feature_id=4')
