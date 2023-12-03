.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	# This runs all of the tests
	pipenv run mypy pyeffects/*.py
	tox

ci:
	pipenv run mypy pyeffects/*.py
	pipenv run py.test --junitxml=pytest.xml --cov-report=term-missing:skip-covered --cov=pyeffects tests/ | tee pytest-coverage.txt


test-readme:
	@pipenv run python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst and HISTORY.rst ok") || echo "Invalid markup in README.rst or HISTORY.rst!"

black:
	pipenv run black --check pyeffects

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=pyeffects tests

coverhtml:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report html --cov=pyeffects tests


publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg pyeffects.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

clean:
	rm -Rf .coverage htmlcov/ .tox .pytest_cache/ .eggs/ pyeffects.egg-info/ build/ dist/
