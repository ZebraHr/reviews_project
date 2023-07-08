# API_Yamdb

## Социальная сеть


## Технологии:
<br>Подробнее:<br>

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue?logo=python)](https://www.python.org/)
[![DjangoRestFramework](https://img.shields.io/badge/DjangoRestFramework%20%7C%203.11-black?logo=django)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite%20%7C%203.11-blue?logo=sqlite)](https://www.sqlite.org/index.html)


## Описание работы:
<br><details><summary>Подробнее</summary><br>

Сервис API для YaMDB - социальной сети, которая собирает отзывы (Review) и оценки пользователей на произведения (Title) в разных категориях и жанрах, а так же комментарии к отзывам. 
Произведения делятся на категории (Category) и жанры (Genres), список которых может быть расширен, но правами на добавление новых жанров, категорий и произведений обладает только администратор. 
Для авторизации пользователей используется код подтверждения.
Для аутентификации пользователей используются JWT-токены.

## Установка и запуск:
<br><details><summary>Подробнее</summary><br>

Клонируйте репозиторий.
Создайте и активируйте виртуальное окружение:
```bash
git clone https://github.com/ZebraHr/api_yamdb.git
cd api_yamdb/
source venv/Scripts/activate
pip install -r requirements.txt
```

Сделайте миграции и запустите проект:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Для управления в админке создайте superuser(а):
```bash
python manage.py createsuperuser
```

### Документация к проекту доступна по адрессу: [![Swagger](https://img.shields.io/badge/Swagger%20%7C%203.11-green?logo=swagger)](127.0.0.1:8000/api/v1/redoc/)


### Проект создан в учебных целях. Авторы:
(https://github.com/T1mBul)
(https://github.com/ZebraHr)
(https://github.com/vikolga)