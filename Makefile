runserver:
	python manage.py run

test:
	sniffer

initdb:
	python manage.py initdb

cleardb:
	python manage.py cleardb

pip:
	pip install -r requirements.txt