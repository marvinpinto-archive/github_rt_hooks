import unittest
from github_rt_hooks.application import app
from github_rt_hooks.pull_request import PullRequest
import json

class TestPullRequest(unittest.TestCase):

    def setUp(self):
        # Use Flask's test client and create a test app every test case can use
        self.test_app = app.test_client()
        self.pull_request_url = app.config['PULL_REQUEST_HOOK_URL']

    def test_pull_request_url_get(self):
        # Make a test request to the app using GET
        response = self.test_app.get(self.pull_request_url)

        # Assert response is 405 METHOD NOT ALLOWED
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")

    def test_pull_request_url_head(self):
        # Make a test request to the app using HEAD
        response = self.test_app.head(self.pull_request_url)

        # Assert response is 405 METHOD NOT ALLOWED
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")

    def test_pull_request_url_options(self):
        # Make a test request to the app using OPTIONS
        response = self.test_app.options(self.pull_request_url)

        # Assert response is 200 OK
        self.assertEquals(response.status, "200 OK")

    def test_pull_request_url_post(self):
        # Make a test request to the app using POST
        response = self.test_app.post(self.pull_request_url)

        # Assert response is 415 UNSUPPORTED MEDIA TYPE
        self.assertEquals(response.status, "415 UNSUPPORTED MEDIA TYPE")

    def test_pull_request_url_post_with_payload(self):
        # Make a test request to the app using POST with some dummy non-json
        # payload
        response = self.test_app.post(self.pull_request_url, data={'username':
            'blah'})

        # Assert response is 415 UNSUPPORTED MEDIA TYPE
        self.assertEquals(response.status, "415 UNSUPPORTED MEDIA TYPE")

    def test_pull_request_url_put(self):
        # Make a test request to the app using PUT
        response = self.test_app.put(self.pull_request_url)

        # Assert response is 405 METHOD NOT ALLOWED
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")

    def test_pull_request_url_delete(self):
        # Make a test request to the app using DELETE
        response = self.test_app.delete(self.pull_request_url)

        # Assert response is 405 METHOD NOT ALLOWED
        self.assertEquals(response.status, "405 METHOD NOT ALLOWED")

    def test_pull_request_url_post_with_incomplete_json(self):

        # Make a test request to the app using POST with some dummy json data
        # but without the Content-Type header 

        json_data = {"username": "xyz", "password": "xyz"}
        response = self.test_app.post(
            self.pull_request_url,
            data=json.dumps(json_data))

        # Assert response is 415 UNSUPPORTED MEDIA TYPE
        self.assertEquals(response.status, "415 UNSUPPORTED MEDIA TYPE")

    def test_pull_request_rt_subject_line(self):
        pr_title = 'Adding expose ports parameter'
        pr_number = '81'
        result = PullRequest.get_rt_email_subject(pr_title, pr_number)
        expected = '[Pull Request] Adding expose ports parameter (#81)'
        self.assertEquals(result, expected)

    def test_pull_request_rt_body(self):
        pr_body = 'Adding expose ports parameter to provide --expose feature in template. Updated documentation to reflect usage.'
        pr_html_url = 'https://github.com/garethr/garethr-docker/pull/81'
        pr_diff_contents = "These are some basic diff contents"
        result = PullRequest.get_rt_email_body(pr_body, pr_html_url, pr_diff_contents)
        expected = '[Pull Request] Brand New Pull Request (#100)'
        expected = """Adding expose ports parameter to provide --expose feature in template. Updated documentation to reflect usage.

You can view, comment on, or merge this Pull Request at:
https://github.com/garethr/garethr-docker/pull/81

Change Summary:
These are some basic diff contents"""
        self.assertEquals(result, expected)

    def test_pull_request_opened_rt_pr_comment_string(self):
        rt_number = '12345'
        rt_url = 'https://rt.example.com'
        pr_action = 'opened'
        expected = 'RT [12345](https://rt.example.com/Ticket/Display.html?id=12345) has been opened to track this Pull Request.'
        result = PullRequest.get_formatted_rt_pr_comment_string(rt_number, rt_url, pr_action)
        self.assertEquals(result, expected)

    def test_pull_request_reopened_rt_pr_comment_string(self):
        rt_number = '12345'
        rt_url = 'https://rt.example.com'
        pr_action = 'reopened'
        expected = 'RT [12345](https://rt.example.com/Ticket/Display.html?id=12345) has been reopened to track this Pull Request.'
        result = PullRequest.get_formatted_rt_pr_comment_string(rt_number, rt_url, pr_action)
        self.assertEquals(result, expected)

    def test_pull_request_empty_rt_pr_comment_string(self):
        rt_number = '12345'
        rt_url = 'https://rt.example.com'
        pr_action = ''
        expected = 'RT [12345](https://rt.example.com/Ticket/Display.html?id=12345) has been  to track this Pull Request.'
        result = PullRequest.get_formatted_rt_pr_comment_string(rt_number, rt_url, pr_action)
        self.assertEquals(result, expected)

    def test_pull_request_merged_rt_pr_merged_comment_string(self):
        is_merged = True
        merged_by = 'bob'
        pr_number = '12345'
        gh_repo = 'marvin/testing-mctesterson-repo'
        expected = 'Pull Request marvin/testing-mctesterson-repo (#12345) has been merged and closed by bob!'
        result = PullRequest.get_formatted_rt_pr_merged_comment_string(is_merged, merged_by, pr_number, gh_repo)
        self.assertEquals(result, expected)

    def test_pull_request_unmerged_rt_pr_merged_comment_string(self):
        is_merged = False
        merged_by = 'bob'
        pr_number = '12345'
        gh_repo = 'marvin/testing-mctesterson-repo'
        expected = 'Pull Request marvin/testing-mctesterson-repo (#12345) has been closed with UNMERGED changes.'
        result = PullRequest.get_formatted_rt_pr_merged_comment_string(is_merged, merged_by, pr_number, gh_repo)
        self.assertEquals(result, expected)

