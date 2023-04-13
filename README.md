# Учебный проект в рамках курса "Python-разработчик" от ЯндексПрактикум. Спринт 13.
## API-сервис для публикации отзывов на произведения, упакованный в контейнеры с помощью Docker
![workflow](https://github.com/alex-zharinov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
---
## Адрес сервера:

https://158.160.56.123/

## Документация проекта:
```
http://158.160.56.123/redoc/
```

## Особенности:

- Система регистрация пользователей и выдача токенов.
- Пользовательские роли для управления и редактированием контентом.
- Подключена система оценивания, комментирование отзывов.

---
## Ресурсы API YaMDb
✅ Ресурс **auth**: аутентификация.    

✅Ресурс **users**: пользователи.

✅Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

✅Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»).

✅Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

✅Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.

✅Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

---
## ⚙ Технологии
- _[Python 3.7.9](https://docs.python.org/3.7/)_
 - _[Django 3.2.16](https://docs.djangoproject.com/en/2.2/)_
 - _[Djoser 2.1.0](https://djoser.readthedocs.io/en/latest/)_
 -  _[Django REST framework](https://www.django-rest-framework.org/)_
- _[Request 2.26](https://pypi.org/project/requests/)_
---
### Запуск проекта в dev-режиме:

- Клонировать репозиторий и перейти в него в командной строке:

```bash
git git@github.com:alex-zharinov/infra_sp2.git
```

```bash
cd api_yamdb
```

- Запустите docker-compose:

```
docker-compose up
```

- Выполните по очереди команды:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py loaddata
```

## ⤵️ Примеры запросов:

 - /redoc/ - документация
 - /api/v1/titles/ - получение списка всех произведений
 - /api/v1/titles/{titles_id}/ - получение информации о произведении

## ⤵️ Пример env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=key
```

## ️ Автор - Жаринов Алексей
