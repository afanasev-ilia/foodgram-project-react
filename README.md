# Foodgram

![foodgram-project](https://github.com/LihieTapki/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание

«Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Документация в формате Redoc:

```HTTP
http://foodgram.servehttp.com/api/docs/
```

Проект доступен по ссылке:

```HTTP
http://foodgram.servehttp.com/
```

### Технологии

Python 3.9
Django 2.2.19

### Запуск проекта на удаленном сервере

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

### Запуск проекта на локально

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

### Шаблон наполнения .env

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```


#### Автор

Илья Афанасьев
