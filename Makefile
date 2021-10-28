venv-create:
	python3 -m venv virtualenv

venv-activate:
	source virtualenv/bin/activate

venv-lock:
	pip3 freeze > requirements.txt

venv-install-all:
	pip3 install -r requirements.txt

venv-install:
	./virtualenv/bin/pip3 install $(package)

api:
	./virtualenv/bin/uvicorn src.api:app --reload

db-refresh:
	rm -rf ./store.db && sqlite3 store.db < ./init.sql
