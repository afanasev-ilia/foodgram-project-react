# Foodgram

![foodgram-project](https://github.com/LihieTapki/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Технологии

![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)
![Django Version](https://img.shields.io/badge/django-2.2.19-green.svg)
![Django REST Framework](https://img.shields.io/badge/djangorestframework-3.14.0-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgres-13.0-blue.svg?logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-1.21+-green.svg?logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-20.10+-blue.svg?logo=docker&logoColor=white)

## Описание

«Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Документация в формате Redoc:

```HTTP
http://foodgram.servehttp.com/api/docs/
```

## Запуск проекта на удаленном сервере

Установить на сервере Docker, Docker Compose

Скопировать на сервер файлы docker-compose.yml, nginx.conf из папки infra:

```bash
scp docker-compose.yml nginx.conf username@IP:/home/username/
```

Запускаем контейнеры Docker:

```bash
docker-compose up -d --build
```

Выполняем миграции:

```bash
docker-compose exec backend python manage.py migrate
```

Создаем суперппользователя:

```bash
docker-compose exec backend python manage.py createsuperuser
```

Собираем статику проекта:

```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

Загружаем ингредиенты в БД:

```bash
python manage.py load_ingredients_csv
```

Останавливаем собранные контейнеры:

```bash
docker-compose down -v 
```

## Запуск проекта на локально

Клонируем репозиторий и переходим в него в командной строке:

```bash
git clone git@github.com:LihieTapki/foodgram-project-react.git
```

```bash
cd infra
```

Запускаем docker-compose:

```bash
docker-compose up -d --build
```

Выполняем миграции:

```bash
docker-compose exec backend python manage.py migrate
```

Создаем суперппользователя:

```bash
docker-compose exec backend python manage.py createsuperuser
```

Собираем статику проекта:

```bash
docker-compose exec backend python manage.py collectstatic --no-input
```

Загружаем ингредиенты в БД:

```bash
python manage.py load_ingredients_csv
```

Останавливаем собранные контейнеры:

```bash
docker-compose down -v 
```

## Шаблон наполнения .env

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```


## Автор

Илья Афанасьев
