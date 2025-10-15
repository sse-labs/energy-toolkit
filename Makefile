.PHONY: test

test:
	sudo .venv/bin/python -m unittest discover -s test -p "*.py"

clean:
	rm -rf  test/__pycache__
	rm -rf  energy_toolkit/__pycache__