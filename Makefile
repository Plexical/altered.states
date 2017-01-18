.PHONY cov:
cov:
	py.test -x --cov altered --cov-config=coverage.ini \
	--cov-report term-missing --cov-report html
