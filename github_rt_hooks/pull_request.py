import logging
import github_payload as gp
from request_tracker import RequestTracker
import requests
import json

log = logging.getLogger(__name__)

class PullRequest:
    def __init__(self, config, request):
        self.config = config
        self.request = request
        self.gh_oauth_token = self.config['GITHUB_OAUTH_TOKEN']


    def get_github_url(self):
        gh_url = self.config['GITHUB_URL']
        # Remove the trailing slash from the URL, if present
        if gh_url.endswith('/'):
            gh_url = gh_url[:-1]
        return gh_url


    def process_request(self):
        # self.log_full_request()

        hook_secret = self.config['PULL_REQUEST_HOOK_SECRET']
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
        pr_action = self.request.json['action']
        pr_title = self.request.json['pull_request']['title']
        pr_number = self.request.json['pull_request']['number']
        pr_body = self.request.json['pull_request']['body']
        pr_html_url = self.request.json['pull_request']['html_url']
        pr_diff_url = self.request.json['pull_request']['diff_url']
        pr_sender = self.request.json['sender']['login']
        pr_diff_contents = self.retrieve_url_contents(pr_diff_url)
        rt_subject = self.get_rt_email_subject(pr_title, pr_number)
        rt_body = self.get_rt_email_body(pr_body, pr_html_url, pr_diff_contents)
        rt_queue = self.config['PULL_REQUEST_RT_QUEUE']
        gh_repo_full_name = self.request.json['repository']['full_name']
        rt = RequestTracker(self.config)
        rt_url = rt.get_request_tracker_url()
        try:
            rt_ticket_number = rt.create_rt_from_pr(pr_sender,
                    rt_subject,
                    rt_body,
                    rt_queue,
                    gh_repo_full_name,
                    pr_number)
            if not self.comment_on_pr_with_rt_number(gh_repo_full_name,
                    pr_number,
                    rt_ticket_number,
                    pr_action,
                    rt_url):
                return 412
            return 200
        except ValueError, e:
            return 412


    def comment_on_pr_with_rt_number(self, repo_name, pr_number, rt_number, pr_action, rt_url):
        comment_str = self.get_formatted_rt_pr_comment_string(rt_number, rt_url, pr_action)
        url = str(self.get_github_url()) + '/repos/' + str(repo_name) + '/issues/'
        url += str(pr_number) + '/comments'
        payload = {'body': str(comment_str)}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url,
                auth=(self.gh_oauth_token, 'x-oauth-basic'),
                data=json.dumps(payload),
                headers=headers)
        if r.status_code != 201:
            log.error('HTTP status ' + str(r.status_code) + ' when attempting to contact ' + str(url))
            log.error(r.text)
            return False

        log.debug('Successfully commented on ' + str(repo_name) + '/' + str(pr_number))
        return True


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
    def get_formatted_rt_pr_comment_string(rt_number, rt_url, pr_action):
        comment = 'RT [' + str(rt_number) + '](' + str(rt_url)
        comment += '/Ticket/Display.html?id=' + str(rt_number) + ') '
        comment += 'has been ' + str(pr_action) + ' to track this Pull Request.'
        return comment


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


