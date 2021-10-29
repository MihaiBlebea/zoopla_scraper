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

docker-build:
	docker build -t zoopla_scraper:v1.0 .

docker-run:
	docker run -d -v $(PWD)/store.db:/code/store.db --name scraper -p 8080:80 zoopla_scraper:v1.0

docker: docker-build docker-run

docker-stop:
	docker stop scraper && docker rm scraper

db-refresh:
	rm -rf ./store.db && sqlite3 store.db < ./init.sql

ansible-deploy:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/deploy_zoopla_scraper.yaml

ansible-remove:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/remove_zoopla_scraper.yaml
