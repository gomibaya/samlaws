# Requirements are in setup.py, so whenever setup.py is changed, re-run installation of dependencies.
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	${PYTHON} -m pip install twine
	${PYTHON} -m pip install --upgrade setuptools wheel
	${PYTHON} -m pip install --upgrade tox pylama bandit
	touch $(VENV_NAME)/bin/activate

$(SDIR)/%.py: venv

