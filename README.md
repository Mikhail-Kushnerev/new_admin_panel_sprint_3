# Админ-панель онлайн-кинотеатра
 
Удобная админка для создании базы фильмов с поддержкой полнотекстового поиска

## Оглавление
- [описание](#описание)
- [технлогии](#техлогии)
- <a href="#structure">структура проекта</a>
- [запуск](#запуск)
- [авторы](#авторы)

## Описание

Админ панель, где администратор может добавлять:
- кинопроизоведения;
- жанры;
- актёров/режисёров и т.д.

## Технологии

- Python
- Django
- PostgreSQL
- ElasticSearch
- API
- Nginx
- Docker

<details open>
  <summary>
    <h2 id="#structure">Структура проекта</h2>
  </summary>

```cmd
new_admin_panel_sprint_2:.
|   .env.example <-- Заполнить своими данными
|   .gitignore
|   docker-compose.yml <-- Сборка контейнеров через Docker
|   Makefile <-- Сборка контейнеров через Makefile
|   README.md
|               
+---app
|   |   docker-entrypoint.sh
|   |   Dockerfile
|   |   manage.py
|   |   README.md
|   |   requirements.txt
|   |   __init__.py
  ...
|   |
|   +---movies
|   |   |
|   |   +---api
|   |   |   |
|   |   |   +---tests <-- Тестирование API, запущенное в контейнере
|   |
|   +---postgres_to_es
|   |   |   load_data.py
|   |   |   main.py  <-- Точка входа для переноса данных с PostgreSQL -> ElasticSearch
|   |   |   README.md
|   |   |   __init__.py
|   |   |   
|   |   +---tests
|   |   |       ETLTests-2.json <-- Тестирование Elastsearch, запущенного в контейнере
...
|   |
|   +---sqlite_to_postgres
|   |   |   db.sqlite
|   |   |   load_data.py <-- Заполнение PostgreSQL БД
|   |   |   models.py
|   |   |   README.md
|   |   |   test_load_data.py
|   |   |   __init__.py
|   |   |
    ...
|   |   |
|           
+---infra
```

</details>

[⬆️Оглавление](#оглавление)

## Запуск

Склонируйте репозиторий
```git
git clone https://github.com/Mikhail-Kushnerev/new_admin_panel_sprint_2
```

Переименуйте файл **.env.example** в **.env** и заполните своими данными.
Пример:
```dotenv
SECRET_KEY='<django-project-secret-key>'
DEBUG=False
HOST=<django-project-host>


ORIGINAL_DB=db.sqlite
TEST_DB=<path-to-original-sqlitedb>

POSTGRES_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='postgres'
POSTGRES_USERNAME='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_HOST='<db-container-name>'
POSTGRES_PORT=5432

ELASTIC_HOST='<es-container-name>'
ELASTIC_PORT=9200
```

Соберите контейнеры из главной директории:
- через **Docker**
    ```docker
    docker-compose up -d --build
    ```
    ИЛИ
- через **Makefile**
    ```
    make build
    ```

Создайте **superuser**:
- в контейнере **backend**
    ```docker
    docker-compose exec backend bash
    ```
    ИЛИ
- через **Makefile**
    ```
    make create-user
    ```

Для заполнения баз данных выполните команду:
- в том же контейнере
    ```python
    python sqlite_to_postgres/load_data.py
    ```
    ИЛИ
- через **Makefile**
    ```python
    make load-db
    ```

Для переноса данных с базы в **ElasticSearch**:
- в том же контейнере
    ```python
    python postgres_to_es/main.py
    ```
    ИЛИ
- через **Makefile**
    ```python
    make load-es
    ```
  [⬆️Оглавление](#оглавление)

## Авторы
[Mikhail Kushnerev](https://github.com/Mikhail-Kushnerev/new_admin_panel_sprint_2)  
[В начало](#админ-панель-онлайн-кинотеатра)