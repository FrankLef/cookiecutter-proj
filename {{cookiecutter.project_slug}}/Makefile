project_name := "igc_etl"
git_user := "FrankLef"
git_email := "https://github.com/FrankLef"
git_repo := "https://github.com/FrankLef/igc_etl.git"

# the first target is the default
all: hello

hello:
	# Reference for customized echo
	# CMD equivalent @echo ^[[101;93;1mHello^[[0m
	# \x1b is ASCII hex for ESC
	# see ANSI escape code at https://ss64.com/nt/syntax-ansi.html
	@echo -e "\x1b[1;36mInfo!\x1b[0m"
	@echo -e "\x1b[1;32mSuccess!\x1b[0m"
	@echo -e "\x1b[1;33mWarning!\x1b[0m"
	@echo -e "\x1b[1;31mError!\x1b[0m"
	# on 1 line
	@echo -e "\x1b[1;37mHello World\x1b[0m"
	# now including a line feed
	@echo -e "\x1b[1;37mHello\x0AWorld\x1b[0m"
	# CMD equivalent @echo ^G, or @echo Alt+007, ASCII hex = \x7
	# make the beep sound
	@echo -e "\x7"

poetry_update:
	@echo -e "\x1b[1;33mThis might take a few minutes when run for the first time.\x1b[0m"
	poetry update
	@echo -e "\x1b[1;32mpoetry update ok!\x1b[0m"
	# use poetry show to check if inconsistency
	poetry show
	@echo -e "\x1b[1;32mpoetry show ok!\x1b[0m"
	@echo -e "\x1b[1;36mcompleted successfully!\x1b[0m"

pre_commit:
	pre-commit install
	@echo -e "\x1b[1;32mpre-commit install ok!\x1b[0m"
	pre-commit autoupdate
	@echo -e "\x1b[1;32mpre-commit autoupdate ok!\x1b[0m"
	@echo -e "\x1b[1;36mcompleted successfully!\x1b[0m"

pre_commit_run:
	pre-commit run --all-files


lint: isort black flake
	@echo -e "\x1b[1;36mcompleted successfully!\x1b[0m"

isort:
	isort .
	@echo -e "\x1b[1;32misort ok!\x1b[0m"

black:
	black src/
	@echo -e "\x1b[1;32mblack ok!\x1b[0m"

flake:
	flake8 --ignore=E501
	@echo -e "\x1b[1;32mflake8 ok!\x1b[0m"

git_init:
	# initialize git_repo
	git init
	git branch -M main
	git remote add origin ${git_repo}
	git add -A
	git -c user.name=${git_user} -c user.email=${git_email} commit -m "initialize"
	git push -u -f origin main
	@echo -e "\x1b[1;32mgit initialized successfully!\x1b[0m"
	@echo -e "\x7"

ignored_dir:
	# create data dir which are in the cookicutter because of .gitignore
	mkdir -p data\raw
	@echo -e "\x1b[1;32mIgnored directories created successfully!\x1b[0m"

test:
	@echo -e "\x1b[1;37mThis is a test\x1b[0m"
