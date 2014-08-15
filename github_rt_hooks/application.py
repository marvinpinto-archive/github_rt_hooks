import logging
from flask import Flask, abort, request
import json

log = logging.getLogger(__name__)
app = Flask(__name__)

from pull_request import PullRequest

# Pull in the appropriate settings
app.config.from_envvar('GITHUBRTHOOKS_SETTINGS')

@app.route('/', methods=['GET', 'POST'])
def index():
    abort(403)

pull_request_url = app.config['PULL_REQUEST_HOOK_URL']
@app.route(pull_request_url, methods=['POST'])
def process_pull_request():
    if request.headers['Content-Type'] == 'application/json':
        pr_instance = PullRequest(app)
        status_code = pr_instance.process_request(request)
        if (status_code != 200):
            abort(status_code)
        else:
            return 'okie\n', 200
    else:
        abort(415)

if __name__ == '__main__':
    app.run()

