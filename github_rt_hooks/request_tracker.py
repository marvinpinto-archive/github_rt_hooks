import logging
from rtkit.resource import RTResource
from rtkit.authenticators import CookieAuthenticator
from rtkit.errors import RTResourceError
import json

log = logging.getLogger(__name__)

class RequestTracker:
    def __init__(self, app):
        self.app = app
        self.rt_username = self.app.config['REQUEST_TRACKER_USERNAME']
        self.rt_password = self.app.config['REQUEST_TRACKER_PASSWORD']
        self.rt_url = self.app.config['REQUEST_TRACKER_URL']

        # Remove the trailing slash from the URL, if present
        if self.rt_url.endswith('/'):
            self.rt_url = self.rt_url[:-1]


    def get_rt_sender(self, sender):
        rt_use_generic_sender = self.app.config['REQUEST_TRACKER_USE_GENERIC_SENDER']
        rt_sender = ''
        if rt_use_generic_sender is True:
            rt_sender = self.app.config['REQUEST_TRACKER_GENERIC_SENDER_ADDRESS']
        else:
            rt_email_domain = self.app.config['REQUEST_TRACKER_EMAIL_DOMAIN']
            rt_sender = sender + '@' + rt_email_domain
        return rt_sender


    def create_rt_from_pr(self, sender, subject, body, queue):
        full_rt_url = self.rt_url + '/REST/1.0/'
        rt_sender = self.get_rt_sender(sender)
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
                'Text' : body.replace('\n', '\n '),
            }
        }

        response = None
        try:
            response = resource.post(path='ticket/new', payload=content,)
        except RTResourceError as e:
            log.error(e.response.status_int)
            log.error(e.response.status)
            log.error(e.response.parsed)

        if response.status_int != 200:
            log.error('HTTP status ' + str(response.status_int) + ' when attempting to contact ' + str(full_rt_url))
            log.error(response.status)
            log.error(response.parsed)
            return response.status

        log.info('Successfully created RT "' + str(subject) + '" from PR initiated by ' + str(rt_sender))
        log.info(response.parsed)
        return 200

