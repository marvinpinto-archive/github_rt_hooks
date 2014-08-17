import unittest
from github_rt_hooks.application import app

class TestMain(unittest.TestCase):

    def setUp(self):
        # Use Flask's test client and create a test app every test case can use
        self.test_app = app.test_client()

    def test_root_url_get(self):
        # Make a test request to the app using GET
        response = self.test_app.get('/')

        # # Assert response is 403 FORBIDDEN.
        self.assertEquals(response.status, "403 FORBIDDEN")

    def test_root_url_head(self):
        # Make a test request to the app using HEAD
        response = self.test_app.head('/')

        # # Assert response is 403 FORBIDDEN.
        self.assertEquals(response.status, "403 FORBIDDEN")

    def test_root_url_options(self):
        # Make a test request to the app using OPTIONS
        response = self.test_app.options('/')

        # # Assert response is 200 OK
        self.assertEquals(response.status, "200 OK")

    def test_root_url_post(self):
        # Make a test request to the app using POST
        response = self.test_app.post('/')

        # # Assert response is 403 FORBIDDEN.
        self.assertEquals(response.status, "403 FORBIDDEN")

    def test_root_url_post_with_payload(self):
        # Make a test request to the app using POST with some dummy payload
        response = self.test_app.post('/', data={'username': 'blah'})

        # # Assert response is 403 FORBIDDEN.
        self.assertEquals(response.status, "403 FORBIDDEN")

    def test_root_url_put(self):
        # Make a test request to the app using PUT
        response = self.test_app.put('/')

        # # Assert response is 405 METHOD NOT ALLOWED
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")

    def test_root_url_delete(self):
        # Make a test request to the app using DELETE
        response = self.test_app.delete('/')

        # # Assert response is 405 METHOD NOT ALLOWED
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")


