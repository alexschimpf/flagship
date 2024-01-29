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

# run mypy type checker using daemon
be-type-check:
	cd backend && mypy --config-file mypy.ini .

# install backend python packages
be-install-reqs:
	pip install -r backend/requirements.txt

# install backend python packages
be-install-dev-reqs:
	pip install -r backend/requirements-dev.txt

# run backend unit tests
be-run-unit-tests:
	PYTHONPATH=./backend python -m pytest --verbose --disable-warnings backend/tests/unit

# run backend api tests
be-run-api-tests:
	./backend/tests/api/run-tests.sh

# run dependencies via docker compose
run-docker-compose-deps:
	cd docker &&\
	docker-compose -f docker-compose-deps.yml down -v --remove-orphans &&\
	docker-compose -f docker-compose-deps.yml up

# get lines of python code
be-size:
	git ls-files | grep '\.py' | xargs wc -l

# get lines of ui code
fe-size:
	git ls-files | grep -e 'frontend/src/app' -e 'frontend/src/components' -e 'frontend/src/context' -e 'frontend/src/lib' | xargs wc -l
