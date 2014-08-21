import logging
from rtkit.resource import RTResource
from rtkit.tracker import Tracker
from rtkit.authenticators import CookieAuthenticator
from rtkit.errors import RTResourceError
import json

log = logging.getLogger(__name__)

class RequestTracker:
    def __init__(self, config):
        self.config = config
        self.rt_username = self.config['REQUEST_TRACKER_USERNAME']
        self.rt_password = self.config['REQUEST_TRACKER_PASSWORD']

        # Settings related to which requester is assigned to this RT
        self.rt_use_generic_sender = self.config['REQUEST_TRACKER_USE_GENERIC_SENDER']
        self.rt_generic_sender = self.config['REQUEST_TRACKER_GENERIC_SENDER_ADDRESS']
        self.rt_sender_email_domain = self.config['REQUEST_TRACKER_EMAIL_DOMAIN']


    def get_request_tracker_url(self):
        rt_url = self.config['REQUEST_TRACKER_URL']
        # Remove the trailing slash from the URL, if present
        if rt_url.endswith('/'):
            rt_url = rt_url[:-1]
        return rt_url


    @staticmethod
    def get_rt_sender(use_generic_sender, generic_sender, sender, email_domain):
        from validate_email import validate_email
        if use_generic_sender:
            if not validate_email(generic_sender):
                error_msg = 'Generic sender email address ' + str(generic_sender) + ' is invalid'
                log.error(error_msg)
                raise ValueError(error_msg)
            log.debug('generic sender is ' + str(generic_sender))
            return generic_sender

        full_email = sender + '@' + email_domain
        if not validate_email(full_email):
            error_msg = 'Full email address ' + str(full_email) + ' is invalid'
            log.error(error_msg)
            raise ValueError(error_msg)
        log.debug('full email is ' + str(full_email))
        return full_email


    def search_for_rt_tickets(self, gh_pr, gh_repo):
        full_rt_url = str(self.get_request_tracker_url()) + '/REST/1.0/'
        tracker = Tracker(full_rt_url,
                self.rt_username,
                self.rt_password,
                CookieAuthenticator)
        query = "'CF.{X-Hub-PR}'='" + str(gh_pr) + "' AND 'CF.{X-Hub-Repo}'='" + str(gh_repo) + "'"
        tickets = tracker.search_tickets(query)
        log.debug('Found ' + str(len(tickets)) + ' RT tickets matching the search criteria: ' + str(query))
        return [x.id for x in tickets]


    def create_rt_from_pr(self,
            sender,
            subject,
            body,
            queue,
            gh_repo_full_name,
            gh_pr):
        full_rt_url = str(self.get_request_tracker_url()) + '/REST/1.0/'
        rt_sender = self.get_rt_sender(self.rt_use_generic_sender,
                self.rt_generic_sender,
                sender,
                self.rt_sender_email_domain)
        resource = RTResource(full_rt_url,
                self.rt_username,
                self.rt_password,
                CookieAuthenticator)

        content = {
            'content': {
                'id': 'ticket/new',
                'Queue': queue,
                'Subject' : subject,
                'Requestor': rt_sender,
                'CF-X-Hub-PR': gh_pr,
                'CF-X-Hub-Repo': gh_repo_full_name,
                'Text' : body.replace('\n', '\n '),
            }
        }

        response = None
        try:
            response = resource.post(path='ticket/new', payload=content,)
        except RTResourceError as e:
            error_msg = str(e.response.status_int) + '\n'
            error_msg += str(e.response.status) + '\n'
            error_msg += str(e.response.parsed) + '\n'
            log.error(error_msg)
            raise ValueError(error_msg)

        if response.status_int != 200:
            error_msg = 'HTTP status ' + str(response.status_int) + ' when attempting to contact ' + str(full_rt_url) + '\n'
            error_msg += str(response.status) + '\n'
            error_msg += str(response.parsed) + '\n'
            log.error(error_msg)
            raise ValueError(error_msg)

        # RT returns a 200 (indicating the ticket was created) yet something
        # else went wrong. Sometimes related to the custom field name being
        # nonexistent or the RT user not having enough permission to read/set
        # this field value.
        # Note that response.parsed is a nested list of tuples,
        # e.g. [[('id', 'ticket/587034')]]
        try:
            _tup = response.parsed[0][0]
            rt_ticket_number = _tup[1].replace('ticket/','')
            log.info('Successfully created RT "' + str(subject) + '" from PR initiated by ' + str(rt_sender))
            log.info('URL: ' + str(self.get_request_tracker_url()) + '/Ticket/Display.html?id=' + str(rt_ticket_number))
            log.info(response.parsed)
            return rt_ticket_number
        except IndexError, e:
            error_msg = 'Something went wrong when attempting to create the RT!\n'
            error_msg += 'Received: ' + str(response.body) + '\n'
            log.error(error_msg)
            raise ValueError(error_msg)

