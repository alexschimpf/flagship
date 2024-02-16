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

# runs dependencies only (e.g. redis, mysql, etc.)
deps:
	docker-compose -f docker-compose-deps.yml up --remove-orphans

# runs deps from clean slate
deps-clean:
	docker-compose -f docker-compose-deps.yml down -v --remove-orphans &&\
	docker-compose -f docker-compose-deps.yml pull &&\
	docker-compose -f docker-compose-deps.yml up --build

# runs dependencies, admin server, flags server, and frontend in dev mode (with reload and debug ports)
dev:
	docker-compose -f docker-compose-dev.yml up --remove-orphans

# runs dev from clean slate
dev-clean:
	docker-compose -f docker-compose-dev.yml down -v --remove-orphans &&\
	docker-compose -f docker-compose-dev.yml pull &&\
	docker-compose -f docker-compose-dev.yml up --build

# run runs dependencies, admin server, flags server, and frontend
flagship:
	docker-compose up -f docker-compose.yml --remove-orphans

# runs flagship from clean slate
flagship-clean:
	docker-compose down -f docker-compose.yml -v --remove-orphans &&\
	docker-compose -f docker-compose.yml pull &&\
	docker-compose -f docker-compose.yml up --build
