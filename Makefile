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

# type check admin backend
admin-type-check:
	cd admin && mypy --config-file mypy.ini .

# install admin python packages
admin-install-reqs:
	pip install -r admin/requirements.txt

# install admin python dev packages
admin-install-dev-reqs:
	pip install -r admin/requirements-dev.txt

# run admin unit tests
admin-run-unit-tests:
	PYTHONPATH=./admin python -m pytest --verbose --disable-warnings admin/tests/unit

# run admin api tests
admin-run-api-tests:
	./admin/tests/api/run-tests.sh

# type check flags backend
flags-type-check:
	cd flags && mypy --config-file mypy.ini .

# install flags python packages
flags-install-reqs:
	pip install -r flags/requirements.txt

# install flags python dev packages
flags-install-dev-reqs:
	pip install -r flags/requirements-dev.txt

# run flags unit tests
flags-run-unit-tests:
	PYTHONPATH=./flags python -m pytest --verbose --disable-warnings flags/tests/unit

# run flags api tests
flags-run-api-tests:
	./flags/tests/api/run-tests.sh

# type check python sdk
sdk-python-type-check:
	cd sdk/python && mypy --config-file mypy.ini .

# run dependencies via docker compose
run-deps:
	cd docker &&\
	docker-compose -f docker-compose-deps.yml up --remove-orphans

# remove existing volumes and run dependencies via docker compose
run-deps-clean:
	cd docker &&\
	docker-compose -f docker-compose-deps.yml down -v --remove-orphans &&\
	docker-compose -f docker-compose-deps.yml up

# get lines of python code
 py-size:
	git ls-files | grep '\.py' | xargs wc -l

# get lines of ui code
fe-size:
	git ls-files | grep -e 'frontend/src/app' -e 'frontend/src/components' -e 'frontend/src/context' -e 'frontend/src/lib' | xargs wc -l
