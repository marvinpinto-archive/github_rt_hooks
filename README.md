## Github RT Hooks

Framework for triggering events in [Request
Tracker](http://bestpractical.com/rt) when interesting things happen on Github.


### Development

- Update `logconfig` in `conf/gunicorn.conf.py` to point to the correct place

- You will need python 2.7, pip, virtualenv, etc.

- Fork this repo

- Clone your fork locally

- `make cleanall`

- `make install`

- `make run`


### Unit Tests

Assuming your development environment is setup:

    make test


### Wheel Packaging

    make wheel


### Contributing

Submit a Pull Request, of course!


### Some nice to have features

- Update an RT ticket with an apprpriate comment whenever a commit is pushed to
Github (assumes the commit message contains an RT:XXXXX string of sorts)

- Update an RT assignee whenever a Pull Request assignee (on Github) changes

- Update the RT ticket with an appropriate comment whenever new code changes
are pushed to a Pull Request

- Update the RT ticket with an appropriate comment whenever new comments are
made on Pull Requests

- Update the RT ticket status whenever a Pull Request is reopened or closed

