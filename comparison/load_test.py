from locust import HttpUser, task, between
import random


class QuickstartUser(HttpUser):

    @task
    def view_item(self):
        n = random.randint(2, 50000)
        self.client.get('/prime?n={0}'.format(n))

