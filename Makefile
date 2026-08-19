.PHONY: test demo check

test:
	python -m unittest discover -s tests -p 'test_*.py'

demo:
	python -m titan.cli demo

check: test
	python -m compileall -q titan tests
