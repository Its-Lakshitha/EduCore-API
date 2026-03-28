PYTHON=python
MANAGE=$(PYTHON) manage.py

# Run development server
run:
	$(MANAGE) runserver

# Make migrations
migrations:
	$(MANAGE) makemigrations

# Apply migrations
migrate:
	$(MANAGE) migrate

# Create superuser
superuser:
	$(MANAGE) createsuperuser

# Lint check
lint:
	ruff check .

# Auto-fix lint issues
lint-fix:
	ruff check . --fix

# Format code
format:
	ruff format .

# Open Django shell
shell:
	$(MANAGE) shell

# Run tests
test:
	$(MANAGE) test

# Collect static files
collectstatic:
	$(MANAGE) collectstatic --noinput