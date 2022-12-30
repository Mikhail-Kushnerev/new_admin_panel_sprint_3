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

# ATTENTION

В случае конфликта при сборке **docker-compose** с сообщением `maybe you mean ...` уберите
в файле **docker-entrypoints.sh**, в первой строчке последние два символа:
```git
#!/bin/bash^M --> #!/bin/bash 
```
P.s. данная ошибка была замечена на ОС семейства **Windows**

<details open>
  <summary>
    <h2 id="#structure">Структура проекта</h2>
  </summary>

```cmd
new_admin_sprint_3:.
|   .env.example  <-- Переменные окружения (настроить под себя)
|   .gitignore
|   docker-compose.yml <-- Сборка контейнеров через Docker
|   Makefile <-- Сборка контейнеров через Makefile
|   README.md
|
+---app  <-- Django проект
|   |
|   +---movies  <-- Django приложение
|   |   |
|   |   +---api  <-- API приложения movies
|   |   |   |
|   |   |   +---tests <-- Тестированиие API, запущенного в контейнере, через Postman
|   |
|   +---sqlite_to_postgres
|   |   |
...
|   |   |  load_data.py  <-- Скрипт для переноса БД с Sqlite в PostgreSQL
...
|   |
+---etc  <-- Конфигурация Nginx
|
\---postgres_to_es
    |   .dockerignore
    |   docker-entrypoint.sh
    |   Dockerfile
    |   load_data.py
    |   main.py  <-- Точка входа для переноса БД с PostgreSQL в ElasticSearch
    |   README.md
    |   requirements.txt
    |   wait-for-es.sh
    |   __init__.py
    |   
    +---tests  <-- Тестирование ElasticSearch, запущенного в контейнере, через Postman
    |       
    \---utils
```

</details>

[⬆️Оглавление](#оглавление)

## Запуск

Склонируйте репозиторий
```git
git clone https://github.com/Mikhail-Kushnerev/new_admin_panel_sprint_3
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
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_HOST='<db-container-name>'
POSTGRES_PORT=5432

ELASTIC_HOST='<es-container-name>'
ELASTIC_PORT=9200

TIME_TO_SLEEP=<set-value>
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

  [⬆️Оглавление](#оглавление)

## Авторы
[Mikhail Kushnerev](https://github.com/Mikhail-Kushnerev/new_admin_panel_sprint_2)  
[В начало](#админ-панель-онлайн-кинотеатра)