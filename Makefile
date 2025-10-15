.PHONY: test run clean lint

test:
	sudo .venv/bin/python -m unittest discover -s test -p "*.py"

run:
	sudo .venv/bin/energy-toolkit measure example_programs.yaml -v

lint:
	pylint energy_toolkit/*.py

clean:
	rm -rf  test/__pycache__
	rm -rf  energy_toolkit/__pycache__