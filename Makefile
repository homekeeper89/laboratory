build_app:
	docker build -t app ./app
run_app:
	docker run -p 8000:5000 app
build_compose:
	docker-compose up -d
ping_app:
	curl http://localhost:8000/ping