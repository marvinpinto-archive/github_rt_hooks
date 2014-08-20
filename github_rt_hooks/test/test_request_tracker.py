import unittest
from github_rt_hooks.request_tracker import RequestTracker

class TestRequestTracker(unittest.TestCase):

    def test_request_tracker_generic_sender_bogus_email(self):
        use_generic_sender = True
        generic_sender = 'bob@.'
        sender = 'bob'
        email_domain = 'home.com'
        self.assertRaises(ValueError,
                RequestTracker.get_rt_sender,
                use_generic_sender,
                generic_sender,
                sender,
                email_domain)

    def test_request_tracker_generic_sender_empty_email(self):
        use_generic_sender = True
        generic_sender = ''
        sender = 'bob'
        email_domain = 'home.com'
        self.assertRaises(ValueError,
                RequestTracker.get_rt_sender,
                use_generic_sender,
                generic_sender,
                sender,
                email_domain)

    def test_request_tracker_generic_sender_valid_email(self):
        use_generic_sender = True
        generic_sender = 'bob@home.com'
        sender = 'bob'
        email_domain = 'home.com'
        result = RequestTracker.get_rt_sender(use_generic_sender,
                generic_sender,
                sender,
                email_domain)
        self.assertEquals(result, 'bob@home.com')

    def test_request_tracker_sender_bogus_email(self):
        use_generic_sender = False
        generic_sender = 'bob@home.com'
        sender = 'bob'
        email_domain = '.'
        self.assertRaises(ValueError,
                RequestTracker.get_rt_sender,
                use_generic_sender,
                generic_sender,
                sender,
                email_domain)

    def test_request_tracker_sender_empty_email(self):
        use_generic_sender = False
        generic_sender = 'bob@home.com'
        sender = ''
        email_domain = ''
        self.assertRaises(ValueError,
                RequestTracker.get_rt_sender,
                use_generic_sender,
                generic_sender,
                sender,
                email_domain)

    def test_request_tracker_sender_valid_email(self):
        use_generic_sender = False
        generic_sender = 'bob@home.com'
        sender = 'bob'
        email_domain = 'home.com'
        result = RequestTracker.get_rt_sender(use_generic_sender,
                generic_sender,
                sender,
                email_domain)
        self.assertEquals(result, 'bob@home.com')



