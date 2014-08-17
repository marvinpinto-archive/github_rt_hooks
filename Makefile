TOP := $(dir $(lastword $(MAKEFILE_LIST)))
SRCDIR=github_rt_hooks
APPNAME=github-rt-hooks
TESTDIR=$(SRCDIR)/test
ENVDIR=env
BUILDDIR=build-env
VIRTUALENV=/usr/bin/virtualenv27
WHEELHOUSE=wheels
CURRENT_DIR = $(shell pwd)
REQTXTPROD=generated-requirements.txt
REQTXTWHEEL=setup-req.txt
REQTXTDEV=setup-devreq.txt
RPMREQS=suggested-rpm-requirements.txt

run:
	GITHUBRTHOOKS_SETTINGS=$(CURRENT_DIR)/conf/settings.py $(ENVDIR)/bin/gunicorn -c conf/gunicorn.conf.py github_rt_hooks.application:app

clean:
	rm -rf $(ENVDIR)
	rm -rf $(BUILDDIR)
	rm -rf $(WHEELHOUSE)/temp
	rm -f $(SRCDIR)/*.pyc
	rm -f $(TESTDIR)/*.pyc
	rm -rf build
	rm -rf dist
	rm -rf $(SRCDIR).egg-info

install: clean
	$(VIRTUALENV) --no-site-packages $(ENVDIR)
	$(ENVDIR)/bin/python setup.py develop
	$(ENVDIR)/bin/pip install -r $(REQTXTDEV)

test:
	rm -f $(SRCDIR)/*.pyc
	rm -f $(TESTDIR)/*.pyc
	GITHUBRTHOOKS_SETTINGS=$(CURRENT_DIR)/conf/settings.py $(ENVDIR)/bin/nosetests -v $(TESTDIR)

wheel: clean
	rm -f $(REQTXTPROD)
	rm -f $(RPMREQS)
	$(VIRTUALENV) --no-site-packages $(ENVDIR)
	$(ENVDIR)/bin/python setup.py install
	$(ENVDIR)/bin/pip freeze > $(REQTXTPROD)
	bin/determine_rpm_deps.sh "$(ENVDIR)" "$(RPMREQS)"
	sed -i '/$(APPNAME)/d' $(REQTXTPROD)
	$(VIRTUALENV) --no-site-packages $(BUILDDIR)
	$(BUILDDIR)/bin/pip install wheel
	rm -rf $(WHEELHOUSE)/*
	mkdir -p $(WHEELHOUSE)/temp/thirdparty
	$(BUILDDIR)/bin/pip wheel -w $(WHEELHOUSE)/temp/thirdparty -r $(REQTXTPROD)
	$(BUILDDIR)/bin/python setup.py bdist_wheel
	mv -f dist/*.whl $(WHEELHOUSE)/temp/
	mv -f $(WHEELHOUSE)/temp/* $(WHEELHOUSE)/
	rm -rf $(WHEELHOUSE)/temp

cleanall: clean
	rm -f $(REQTXTPROD)
	rm -f $(RPMREQS)
	rm -rf $(WHEELHOUSE)

