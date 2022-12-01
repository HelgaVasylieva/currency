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

gunicorn:
	cd app && gunicorn settings.wsgi:application \
											--bind 0.0.0.0:8000 \
											--workers 8 \
											--threads 2 \
											--log-level debug \
											--max-requests 1000 \
											--timeout 10

uwsgi:
	cd app && uwsgi --module=settings.wsgi:application \
					--master \
					--http=0.0.0.0:8001 \
					--workers 8 \
					--enable-threads \
					--threads 2 \
					--harakiri=10 \
					--max-requests=1000 \

