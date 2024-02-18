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

setup-dev:
	make install-dev &&\
	make install-pre-commit

install-dev:
	npm --prefix frontend install frontend &&\
	pip install -r requirements.txt &&\
	make -C admin install-dev &&\
	make -C flags install-dev &&\
	make -C sdk/python install-dev

install-pre-commit:
	pre-commit install --hook-type pre-commit

all-tests:
	make -C admin unit-tests &&\
	make -C flags unit-tests &&\
	make -C admin api-tests &&\
	make -C flags api-tests

format:
	make -C admin format &&\
	make -C flags format &&\
	make -C sdk/python format &&\
	npm --prefix frontend run format

loc:
	git ls-files | grep -e '\.py' -e 'frontend/src' -e 'sdk/javascript/.*\\.js' | xargs wc -l
