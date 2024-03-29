GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# help
TARGET_MAX_CHAR_NUM=20
help:
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

# run ruff formatter
format:
	ruff format **/

# run ruff linter
lint:
	ruff check --fix **/

# type-check python
type-check:
	mypy .

# install requirements
install:
	pip install -r requirements.txt

# install dev requirements
install-dev:
	pip install -r requirements-dev.txt

# run unit tests
unit-tests:
	PYTHONPATH=. python -m pytest --verbose --disable-warnings tests/unit

# run api tests
api-tests:
	./tests/api/run-tests.sh
