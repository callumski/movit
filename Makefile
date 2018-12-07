VIRTUALENV=env
V_PATH=$(VIRTUALENV)/bin
V_COMMAND=source $(V_PATH)/activate;
BOARD="movit/default_board.json"

.PHONY: all clean setup test run run-profile

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

test:
	$(V_COMMAND) py.test --verbose --flake8 --isort

run:
	$(V_COMMAND) python3 movit/movit.py ${BOARD}

run-json:
	@$(V_COMMAND) python3 movit/movit.py --json-output ${BOARD}

run-profile:
	$(V_COMMAND) python -m cProfile -s cumtime movit/movit.py ${BOARD}

run-ten:
	$(V_COMMAND) python3 movit/movit.py --find-n 10 ${BOARD}

run-ten-json:
	@$(V_COMMAND) python3 movit/movit.py --find-n 10 --json-output ${BOARD}

run-ten-profile:
	$(V_COMMAND) python -m cProfile -s cumtime movit/movit.py --find-n 10 ${BOARD}

run-all:
	$(V_COMMAND) python3 movit/movit.py --find-all ${BOARD}

run-all-profile:
	$(V_COMMAND) python -m cProfile -s cumtime movit/movit.py --find-all ${BOARD}


