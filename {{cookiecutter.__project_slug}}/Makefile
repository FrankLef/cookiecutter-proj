git_user := "{{cookiecutter.git_user}}"
git_email := "{{cookiecutter.git_email}}"
git_repo := "{{cookiecutter.git_repo}}"

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

precommit:
	pre-commit install
	@echo -e "\x1b[1;32mpre-commit install ok!\x1b[0m"
	pre-commit autoupdate
	@echo -e "\x1b[1;32mpre-commit autoupdate ok!\x1b[0m"
	@echo -e "\x1b[1;36mcompleted successfully!\x1b[0m"

precommit_run:
	pre-commit run --all-files

lint:
	ruff check .
	@echo -e "\x1b[1;32mlint completed successfully with ruff!\x1b[0m"

format:
	ruff format .
	@echo -e "\x1b[1;32mformat completed successfully with ruff!\x1b[0m"

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
	mkdir -p data/d0_temp
	mkdir -p data/d1_extr
	mkdir -p data/d2_transf
	mkdir -p data/d3_load
	mkdir -p data/d4_raw
	mkdir -p data/d5_preproc
	mkdir -p data/d6_eda
	mkdir -p data/d7_final
	@echo -e "\x1b[1;32mIgnored directories created successfully!\x1b[0m"

test:
	@echo -e "\x1b[1;37mThis runs pytest\x1b[0m"
	pytest
