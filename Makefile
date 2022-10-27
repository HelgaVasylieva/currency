SHELL := /bin/bash

manage_py := python app/manage.py

manage:
	$(manage_py) $(COMMAND)

run:
	$(manage_py) runserver 0:8000

show_urls:
	$(manage_py) show_urls

migrate:
	$(manage_py) migrate

makemigrations:
	$(manage_py) makemigrations

shell:
	$(manage_py) shell_plus --print-sql

celery:
	cd app && celery -A settings worker --loglevel=INFO

celerybeat:
	cd app && celery -A settings beat --loglevel=INFO

pytest:
	pytest app/tests/

coverage:
	pytest --cov=app app/tests/ --cov-report html && coverage report --fail-under=79.0000

show-coverage:  ## open coverage HTML report in default browser
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"
