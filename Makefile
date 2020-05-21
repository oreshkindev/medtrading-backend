.PHONY: clean system-packages python-packages install run update-db all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip install -r requirements.txt

install: system-packages python-packages

run:
	python manage.py run

update-db:
	python manage.py db migrate --message 'initial database migration'
	python manage.py db upgrade

all: clean install run
