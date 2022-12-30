build:
	docker-compose up -d --build

create-user:
	docker-compose exec backend bash -c "python manage.py createsuperuser"
