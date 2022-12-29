build:
	docker-compose up -d --build

create-user:
	docker-compose exec backend bash -c "python manage.py createsuperuser"

load-db:
	docker-compose exec backend bash -c "cd sqlite_to_postgres && python load_data.py"

load-es:
	docker-compose exec backend bash -c "cd postgres_to_es && python main.py"