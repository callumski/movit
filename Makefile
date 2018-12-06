VIRTUALENV=env
V_PATH=$(VIRTUALENV)/bin
V_COMMAND=source $(V_PATH)/activate;
BOARD="movit/profile_test_board.json"

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

run-profile:
	$(V_COMMAND) python -m cProfile -s cumtime movit/movit.py ${BOARD}
