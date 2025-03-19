.PHONY: test coverage clean

test:
	pytest

coverage:
	pytest --cov=modules --cov-report=term-missing --cov-report=html tests/

clean:
	rm -rf htmlcov/
	rm -f .coverage
