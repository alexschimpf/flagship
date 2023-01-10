## Common

GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# help
TARGET_MAX_CHAR_NUM=20
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

# run mypy type checker using daemon
type-check:
	mypy .

# enable commit hook for python linter
enable-linter:
	pre-commit install -c .pre-commit.yaml

# disable commit hook for python linter
disable-linter:
	pre-commit uninstall -c .pre-commit.yaml

# set up pre-configured pycharm run configurations
setup-pycharm-run-configs:
	find . -name "*.run.xml" -type f -delete && for file in ./.pycharm/*; do cp "$$file" "$${file%.xml}.run.xml"; done;

install-dev-reqs:
	pip install -r requirements.dev.txt

## Server

# install dev and prod python server dependencies
install-server-reqs:
	pip install -r server/requirements.txt

# run server unit tests
run-server-unit-tests:
	PYTHONPATH=./server python -m pytest -v server/tests/unit

# run server api tests
run-server-api-tests:
	./server/tests/api/runtests.sh
