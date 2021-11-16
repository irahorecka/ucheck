black: ## Black format every python file to line length 100
	find . -type f -name "*.py" | xargs black --line-length=100;
	find . -type f -name "*.py" | xargs absolufy-imports;
	make clean;

flake8: ## Flake8 every python file
	find . -type f -name "*.py" -a | xargs flake8;

pylint: ## pylint every python file
	find . -type f -name "*.py" -a | xargs pylint;

pre-commit: ## Install and autoupdate pre-commit
	pre-commit install;
	pre-commit autoupdate;

build: ## Build package distribution files
	flit build;

publish: ## Publish package distribution files to pypi
	flit publish;
	make clean;

clean: ## Remove package distribution files and pycache
	rm -rf ./ucheck.egg-info ./dist ./build;
	find . -type d -name "__pycache__" | xargs rm -r;
