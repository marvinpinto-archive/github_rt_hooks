import logging
from github_rt_hooks import __version__

class VersionLogFormatter(logging.Formatter):

    def format(self, record):
        record.__dict__['version'] = __version__
        return logging.Formatter.format(self, record)

