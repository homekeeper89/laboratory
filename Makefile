# TODO env param 으로 받아서 작동하도록 변경
# build_compose ${env}:
# 	docker-compose --env-file .env.${env} up -d

build_compose_dev:
	docker-compose --env-file .env.dev up -d

build_app:
	docker build -t app ./app

run_app:
	docker run -p 8000:5000 app


ping_app:
	curl http://localhost:8000/ping

sync_db:
	flask-sqlacodegen "mysql+mysqlconnector://root:root@localhost:3306/practice" --flask > models.py 