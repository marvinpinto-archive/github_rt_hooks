import logging
import github_payload as gp
from request_tracker import RequestTracker
import requests

log = logging.getLogger(__name__)

class PullRequest:
    def __init__(self, app, request):
        self.app = app
        self.request = request


    def process_request(self):
        # self.log_full_request()

        hook_secret = self.app.config['PULL_REQUEST_HOOK_SECRET']
        if not gp.validate_github_paylod(self.request, hook_secret):
            return 403

        # Make sure the 'action' key actually exists in request.json before
        # attempting to process it
        if 'action' not in self.request.json:
            # The 'action' key we base things around isn't present so not going
            # to bother continuing
            log.debug('"action" key not present - ignoring and moving on')
            return 200

        action = self.request.json['action']

        # Source: https://developer.github.com/webhooks
        # The action name associated with the pull_request events can be one of
        # assigned, unassigned, labeled, unlabeled, opened, closed, reopened,
        # or synchronized 
        log.debug('Received action "' + str(action) + '"')
        if action == 'opened':
            return self.create_new_rt_from_pull_request()
        elif action == 'reopened':
            return self.create_new_rt_from_pull_request()
        else:
            # We don't care about any of the other action events just yet
            log.debug('Ignoring action "' + str(action) + '"')
            return 200


    def create_new_rt_from_pull_request(self):
        pr_title = self.request.json['pull_request']['title']
        pr_number = self.request.json['pull_request']['number']
        pr_body = self.request.json['pull_request']['body']
        pr_html_url = self.request.json['pull_request']['html_url']
        pr_diff_url = self.request.json['pull_request']['diff_url']
        pr_sender = self.request.json['sender']['login']
        pr_diff_contents = self.retrieve_url_contents(pr_diff_url)
        rt_subject = self.get_rt_email_subject(pr_title, pr_number)
        rt_body = self.get_rt_email_body(pr_body, pr_html_url, pr_diff_contents)
        rt_queue = self.app.config['PULL_REQUEST_RT_QUEUE']
        rt = RequestTracker(self.app.config)
        rt_ticket_http_response = rt.create_rt_from_pr(pr_sender, rt_subject, rt_body, rt_queue)
        return rt_ticket_http_response


    def retrieve_url_contents(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            log.error('http status ' + str(r.status_code) + ' when attempting to contact ' + str(url))
            return "*** Could not retrieve diff contents ***"
        return r.text


    def log_full_request(self):
        # Log the request headers
        log.debug('Raw request headers: ' + str(self.request.headers))

        # Log the request body as well
        log.debug('Raw POST data: ' + json.dumps(self.request.json))


    @staticmethod
    def get_rt_email_subject(pr_title, pr_number):
        return '[Pull Request] ' + str(pr_title) + ' (#' + str(pr_number) + ')'


    @staticmethod
    def get_rt_email_body(pr_body, pr_html_url, pr_diff_contents):
        email_body = [pr_body + '\n',
                'You can view, comment on, or merge this Pull Request at:',
                pr_html_url + '\n',
                'Change Summary:',
                pr_diff_contents]
        return '\n'.join(email_body)


