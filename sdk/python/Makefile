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

# build python package
build:
	echo 'build'

# install package (after running `make build`)
install-build:
	echo 'install-build'

# deploy to pypi
deploy:
	twine upload dist/*

# run ruff formatter
format:
	ruff format **/

# run ruff linter
lint:
	ruff check **/

# type-check python
type-check:
	mypy .

# install requirements
install:
	pip install -r requirements.txt

# install dev requirements
install-dev:
	pip install -r requirements-dev.txt
