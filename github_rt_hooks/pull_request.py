import logging
import github_payload as gp
from request_tracker import RequestTracker
import requests

log = logging.getLogger(__name__)

class PullRequest:
    def __init__(self, app):
        self.app = app


    def process_request(self, request):
        # self.log_full_request(request)

        hook_secret = self.app.config['PULL_REQUEST_HOOK_SECRET']
        if not gp.validate_github_paylod(request, hook_secret):
            return 403

        # Make sure the 'action' key actually exists in json.data before
        # attempting to process it
        if 'action' not in json.data:
            # The 'action' key we base things around isn't present so not going
            # to bother continuing
            log.debug('"action" key not present - ignoring and moving on')
            return 200

        action = request.json['action']
        if action not in 'opened reopened':
            # We don't care about the assigned, unassigned, labeled, unlabeled,
            # closed, or synchronized actions at the moment.
            log.debug('Received and ignored action "' +str(action) +'"')
            return 200

        # We only care about the 'opened' and 'reopened' actions here
        pr_title = request.json['pull_request']['title']
        pr_number = request.json['pull_request']['number']
        pr_body = request.json['pull_request']['body']
        pr_html_url = request.json['pull_request']['html_url']
        pr_diff_url = request.json['pull_request']['diff_url']
        pr_sender = request.json['sender']['login']
        pr_diff_contents = self.retrieve_url_contents(pr_diff_url)
        rt_subject = self.get_rt_email_subject(pr_title, pr_number)
        rt_body = self.get_rt_email_body(pr_body, pr_html_url, pr_diff_contents)
        rt_queue = self.app.config['PULL_REQUEST_RT_QUEUE']
        rt = RequestTracker(self.app)
        rt_ticket_response = rt.create_rt_from_pr(pr_sender, rt_subject, rt_body, rt_queue)

        return rt_ticket_response


    def retrieve_url_contents(self, url):
        return_value = "***Could not retrieve diff contents***"
        r = requests.get(url)
        if r.status_code != 200:
            log.error('http status ' +str(r.status_code)+ ' when attempting to contact ' +str(url))
            return "*** Could not retrieve diff contents ***"
        else:
            return r.text


    def log_full_request(self, request):
        # Log the request headers
        log.debug('Raw request headers: ' + str(request.headers))

        # Log the request body as well
        log.debug('Raw POST data: ' + json.dumps(request.json))


    @staticmethod
    def get_rt_email_subject(pr_title, pr_number):
        return '[Pull Request] ' +str(pr_title)+ ' (#' +str(pr_number)+ ')'


    @staticmethod
    def get_rt_email_body(pr_body, pr_html_url, pr_diff_contents):
        email_body = [pr_body + '\n',
                'You can view, comment on, or merge this Pull Request at:',
                pr_html_url + '\n',
                'Change Summary:',
                pr_diff_contents]
        return '\n'.join(email_body)


