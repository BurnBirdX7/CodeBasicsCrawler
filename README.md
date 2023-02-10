
# CodeBasics scrapper

Собирает данные о курсах с платформы [CodeBasics](https://code-basics.com/ru).

## Требования

Python-пакеты:
 * `scrapy` - Скраппер
 * `psycopg2` - PostgreSQL адаптер
 * `python-dotenv` - Загрузка переменных окржения из `.env` файла

```shell
python3 -m pip install scrapy psycopg2 python-dotenv
```

## Запуск

Сбор данных с платформы CodeBasics и обновление БД

```shell
python3 main.py
```

Чтобы подключиться к базе данных нужно описать конфигурацию в `config.py`.\
С конфигурацией по умолчанию пароль для БД можно задать через переменную окружения `DB_PASSWORD`
(или через файл `.env`).


## Конфигурация

В `config.py` нужно указать данные для подключения к БД, а также можно поменять переопределить
название сущностей 
