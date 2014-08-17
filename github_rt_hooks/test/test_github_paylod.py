import unittest
import github_rt_hooks.github_payload as gp


class TestGithubPayload(unittest.TestCase):

    def test_github_signature_header_empty_values(self):
        header = {}
        result = gp.does_github_signature_header_exist(header)
        self.assertFalse(result)

    def test_github_signature_header_single_bogus_value(self):
        header = {'bogus': 1234}
        result = gp.does_github_signature_header_exist(header)
        self.assertFalse(result)

    def test_github_signature_header_multiple_bogus_values(self):
        header = {'bogus1': 1234, 'bogus2': 1234}
        result = gp.does_github_signature_header_exist(header)
        self.assertFalse(result)

    def test_github_signature_header_single_with_correct_value(self):
        header = {'X-Hub-Signature': 'sha1=1234'}
        result = gp.does_github_signature_header_exist(header)
        self.assertTrue(result)

    def test_github_signature_header_multiple_with_correct_values(self):
        header = {'X-Hub-Signature': 'sha1=1234', 'bogus': 1234}
        result = gp.does_github_signature_header_exist(header)
        self.assertTrue(result)

    def test_github_signature_header_with_incorrect_case(self):
        header = {'X-hub-signature': 'sha1=1234'}
        result = gp.does_github_signature_header_exist(header)
        self.assertFalse(result)

    def test_github_header_with_non_sha1(self):
        header = {'X-hub-signature': 'sha2=1234'}
        data = ''
        secret = 'secret123'
        result = gp.is_github_signature_valid(header, data, secret)
        self.assertFalse(result)

    def test_github_header_signature_does_not_exist(self):
        header = {'X-hub-signaturE': 'sha2=1234'}
        data = ''
        secret = 'secret123'
        result = gp.is_github_signature_valid(header, data, secret)
        self.assertFalse(result)

    def test_github_header_valid_paylod(self):
        header = {'X-Hub-Signature': 'sha1=f5dae278f876c3eb2f304419440d374ba4c6f070'}
        data = 'This is some raw payload'
        secret = 'secret123'
        result = gp.is_github_signature_valid(header, data, secret)
        self.assertTrue(result)

    def test_github_header_incorrect_secret(self):
        header = {'X-Hub-Signature': 'sha1=f5dae278f876c3eb2f304419440d374ba4c6f070'}
        data = 'This is some raw payload'
        secret = 'secret1234'
        result = gp.is_github_signature_valid(header, data, secret)
        self.assertFalse(result)

    def test_github_header_incorrect_payload_vs_sha1(self):
        header = {'X-Hub-Signature': 'sha1=f5dae278f876c3eb2f304419440d374ba4c6f070'}
        data = 'This is some raw payload with a minor tweak'
        secret = 'secret123'
        result = gp.is_github_signature_valid(header, data, secret)
        self.assertFalse(result)

