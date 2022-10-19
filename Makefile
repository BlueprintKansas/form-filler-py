test:
	PYTHONPATH='.' pytest -s -vv

test-cli:
	@PYTHONPATH='.' python -m formfiller --image=test-base-image.png --payload=form-payload.json --form=form-definition.json

build:
	python setup.py build

deps:
	python setup.py install
	pip install -U -r requirements.txt
	pip install pytest black flake8

distcheck:
	python setup.py sdist

dist:
	python setup.py sdist upload

lint:
	flake8 formfiller/*py tests/*py
	black formfiller/*py tests/*py

.PHONY: test build deps distcheck dist lint
