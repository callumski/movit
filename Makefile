VIRTUALENV=env
V_PATH=$(VIRTUALENV)/bin
V_COMMAND=source $(V_PATH)/activate;

.PHONY: all clean setup test run

all: clean setup test

clean:
	rm -f crawlit/*.pyc
	rm -rf $(VIRTUALENV)
	rm -rf output

setup:
	python3 -m venv $(VIRTUALENV)
	$(V_COMMAND) pip install --upgrade setuptools
	$(V_COMMAND) pip install -r requirements.txt
	$(V_COMMAND) pip install -e .
	mkdir output

test:
	$(V_COMMAND) python3 -m pytest --verbose

run:
	$(V_COMMAND) python3 movit/movit.py "movit/default_board.json"
