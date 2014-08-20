DEBUG = False
PULL_REQUEST_HOOK_URL = '/pull_request_testing'
PULL_REQUEST_HOOK_SECRET = 'sekrit123'
PULL_REQUEST_RT_QUEUE = 'Fake-RT-Queue-That-Does-Not-Exist'
REQUEST_TRACKER_USERNAME = 'rt-user-with-appropriate-privs'
REQUEST_TRACKER_PASSWORD = '123sekrit'
REQUEST_TRACKER_URL = 'https://rt.example.com'
REQUEST_TRACKER_USE_GENERIC_SENDER = False
REQUEST_TRACKER_GENERIC_SENDER_ADDRESS = 'bob@example.com'
REQUEST_TRACKER_EMAIL_DOMAIN = 'example.com'
GITHUB_USER = 'github-username'
GITHUB_OAUTH_TOKEN = 'github-oauth-token-for-above-user'
# When working with GitHub Enterprise don't forget to add the /api/v3/ path
GITHUB_URL = 'https://api.github.com'

