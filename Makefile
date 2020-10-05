# Shell to use
SHELL := /bin/bash

# The directory of this file
MY_DIR := $(shell echo $(shell cd "$(shell dirname "${BASH_SOURCE[0]}" )" && pwd ))
APP_DIR := $(MY_DIR)/grodt_test_project
VENV_DIR := $(MY_DIR)/.venv3
DOCKERFILE := $(MY_DIR)/docker-compose-devel.yml

# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
# based on: https://stackoverflow.com/questions/10858261/abort-makefile-if-variable-not-set
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

# https://stackoverflow.com/questions/1789594/how-do-i-write-the-cd-command-in-a-makefile
CHDIR_SHELL := $(SHELL)
define chdir
   $(eval _D=$(firstword $(1) $(@D)))
   $(info $(MAKE): cd $(_D)) $(eval SHELL = cd $(_D); $(CHDIR_SHELL))
endef

# grep the version from the mix file
# VERSION=$(shell ./version.sh)

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help venv_install_requirements venv_new venv_remove clean_all clean_deep start_devel stop_devel restart_devel test

help: ## This help
		@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

#
# virtual env tasks
#
venv_install_requirements: venv_new ## install python packages
		# test -d $(VENV_DIR) && $(VENV_DIR)/bin/pip install --no-cache -r $(APP_DIR)/requirements/local.txt
		test -d $(VENV_DIR) && $(VENV_DIR)/bin/pip install -r requirements/devel.txt

venv_new: venv_remove ## create new venv
		test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

venv_remove: ## remove venv
		-test -d $(VENV_DIR) && rm -rf $(VENV_DIR)

#
# clean up tasks
#
clean_deep: clean_all ## also removes all docker images, containers and volumes
		-@docker rm -f $$(docker ps -a -q) 2>&1 >/dev/null
		-@docker rmi -f $$(docker images -q) 2>&1 >/dev/null
		-docker volume ls
		-@docker volume prune -f 2>&1 >/dev/null

clean_all: ## Clean up migrations, pychache and db in APP_DIR
		-sudo chown -R $$(sudo printenv SUDO_USER). .
		-for i in `find $(APP_DIR) -iname "migrations" -type d`; do rm -rf $${i}/00*; echo; done 2>&1 >/dev/null
		-find $(APP_DIR) -iname "__pycache__" -type d -exec rm -rf \{\} \; ; 2>&1 >/dev/null
		-find $(APP_DIR) -iname "*.pyc" -type f -exec rm -rf \{\} \; ; 2>&1 >/dev/null
		-rm -rf *.sqlite3 *.log *.pid .mypy_cache .pytest_cache .ipython staticfiles .coverage 2>&1 >/dev/null

#
# grodt_test_project tasks
#
start_devel: ## start development (devel) docker containers
		-docker-compose -f $(DOCKERFILE) up -d --build

stop_devel: ## stop development (devel) docker containers
		-docker-compose -f $(DOCKERFILE) down
		-docker-compose -f $(DOCKERFILE) down


restart_devel: stop_devel clean_all start_devel ## restart development (devel) docker containers

#
# project test tasks
#
test:  ## run all tests for project
		@echo "    _    ____  ____    _           _             _           _   ___ _ "
		@echo "   / \  |  _ \|  _ \  (_)___   ___| |_ __ _ _ __| |_ ___  __| | |__ \ |"
		@echo "  / _ \ | |_) | |_) | | / __| / __| __/ _\` | '__| __/ _ \/ _\` |   / / |"
		@echo " / ___ \|  __/|  __/  | \__ \ \__ \ || (_| | |  | ||  __/ (_| |  |_||_|"
		@echo "/_/   \_\_|   |_|     |_|___/ |___/\__\__,_|_|   \__\___|\__,_|  (_)(_)"
		@echo ""
		@read -p "Continue? [ENTER/CTRL+C] " -n1 -s
		@echo ""
		docker-compose -f $(DOCKERFILE) run --rm django python /app/manage.py collectstatic --noinput
		docker-compose -f $(DOCKERFILE) run --rm django python /app/manage.py test
		docker-compose -f $(DOCKERFILE) run --rm django pytest
		docker-compose -f $(DOCKERFILE) run --rm django coverage run -m pytest
		docker-compose -f $(DOCKERFILE) run --rm django mypy -m grodt_test_project

#
# other tasks
#
logs: ## show Docker container logs
		-docker-compose -f $(DOCKERFILE) logs -f

shell_django: ## create a shell in django container
		-docker-compose -f $(DOCKERFILE) exec django /bin/bash
