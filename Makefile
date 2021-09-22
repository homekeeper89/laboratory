build_app:
	docker build -t app ./app
run_app:
	docker run -p 8000:5000 app
ping_app:
	curl http://127.0.0.1:8000/ping