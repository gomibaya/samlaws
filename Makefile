# Valor VIRTUAL para utilizar venv o sin valor para utilizar los recursos ya instalados en el sistema, por ejemplo
# si se utilizxa dentro de un docker con todo lo necesario ya instalado.
#BUILDENV?=VIRTUAL
# Directorio en el que está el código
SDIR=src

# No modificar a partir de aqui, salvo que sea extrictamente necesario
VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
INCLUDESRCS=srcs.mk
SDIR_PATH:=$(shell dirname $(realpath $(SDIR)))

ifeq ($(BUILDENV),VIRTUAL)
  PYTHON=${VENV_NAME}/bin/python3
  BANDIT=${VENV_NAME}/bin/bandit
  PYLAMA=$(PYTHON) -m pylama
  buildpre=venv
  INCLUDEVENV=venv.mk
  PREFIXVAR=
.PHONY: help lint validate test securitylint clean clean-build clean-pyc clean-bandit clean-tox clean-venv clean-output clean-eclipse build publishpip publishpiptest
else
  PYTHON=python3
  BANDIT=bandit
  PYLAMA=pylama
  buildpre=
  INCLUDEVENV=
  PREFIXVAR=/pythondev/
.PHONY: help lint validate test securitylint clean clean-build clean-pyc clean-bandit clean-tox clean-venv clean-output clean-eclipse build publishpip publishpiptest
endif

ODIR=$(PREFIXVAR)output
TDIR=tests
-include $(INCLUDESRCS)

SRCS = $(patsubst %,$(SDIR)/%,$(_SRCS))
LINTS = $(patsubst %,$(ODIR)/%.lint,$(_SRCS))
SECURES = $(patsubst %,$(ODIR)/%.secure,$(_SRCS))
TESTS = $(patsubst %,$(ODIR)/test_unit_%.test,$(_SRCS))

.DEFAULT: help
help:
ifeq ($(BUILDENV),VIRTUAL)
	@echo "make venv"
	@echo "       prepare python virtual environment"
endif
	@echo "make lint"
	@echo "       run pylama"
	@echo "make test"
	@echo "       run tests"
	@echo "make full"
	@echo "       check all the python files in projects"
#	@echo "make run"
#	@echo "       run project"
#	@echo "make doc"
#	@echo "       build sphinx documentation"
	@echo "make clean"
	@echo "       clean project"
	@echo "make publishpip"
	@echo "       publish in pypi.org"
	@echo "make publishpiptest"
	@echo "       publish in test.pypi.org"
	
#prepare-dev:
#	sudo apt-get -y install python3 python3-pip
#	python3 -m pip install virtualenv
#	make venv
-include $(INCLUDEVENV)

test: $(TESTS)

lint: $(LINTS)

secure: $(SECURES)
    
$(ODIR)/%.py.lint: $(SDIR)/%.py
	@echo "*** lint $< ***"
	@if [ ! -d $$(dirname $@) ]; then mkdir -p $$(dirname $@); fi
	@${PYLAMA} --report $@  $< && echo "success!" || { cat $@; rm $@; exit 1; }

$(ODIR)/%.py.secure: $(SDIR)/%.py
	@echo "*** bandit $< ***"
	@if [ ! -d $$(dirname $@) ]; then mkdir -p $$(dirname $@); fi
	@${BANDIT} -f txt -o $@  $< && echo "success!" || { cat $@; rm $@; exit 1; }

$(ODIR)/%.py.test: $(TDIR)/%.py
	@echo "*** test $< ***"
	@if [ ! -d $$(dirname $@) ]; then mkdir -p $$(dirname $@); fi
	@export PYTHONDONTWRITEBYTECODE=1
	@PYTHONPATH=${SDIR_PATH}/${SDIR} ${PYTHON} $< > $@ 2>&1 && echo "success!" || { cat $@; rm $@; exit 1; }
		
full: $(LINTS) $(SECURES) $(TESTS)
    
#run: venv
#    ${PYTHON} app.py

#doc: venv
#    $(VENV_ACTIVATE) && cd docs; make html

clean: clean-pyc clean-bandit clean-build clean-tox clean-output

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-bandit:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean-venv:
	test ! -d ${VENV_NAME} || rm -rf ${VENV_NAME}
	
	
clean-output: 
# utilizo la forma test ! -d ${ODIR] en vez de test -d ${ODIR} para que el test no devuelva 1, sino genera error el make
	test ! -d ${ODIR} || find ${ODIR} -name '*.py.lint' -exec rm -f {} +
	test ! -d ${ODIR} || find ${ODIR} -name '*.py.secure' -exec rm -f {} +
	test ! -d ${ODIR} || find ${ODIR} -name '*.py.test' -exec rm -f {} +
	rm -rf ${ODIR}

clean-tox:
	rm -rf .tox/

clean-eclipse:
	rm -f .project
	rm -f .pydevproject
	rm -rf .settings/


build: lint test securitylint
	${PYTHON} setup.py sdist bdist_wheel

validate:
	tox
	
publishpip: build
	${PYTHON} -m twine upload dist/*
	
publishpiptest: build
	${PYTHON} -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

