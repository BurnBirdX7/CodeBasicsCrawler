
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

### Scrape and save to file

Соберёт данные с CodeBasics и поместит в выходной файл

В корне проекта запустить
```shell
scrapy crawl CodeBasics -o out.csv
```

Ключ `-o` описывает выходной файл.
Точно поддерживаются форматы CSV и JSON.

### Scrape and post to DB
Соберёт данные с CodeBasics и обновит базу данных

```shell
python3 main.py
```

Чтобы подключиться к базе данных нужно описать конфигурацию в `config.py`.\
С конфигурацией по умолчанию пароль для БД можно задать через переменную окружения `DB_PASSWORD`
(или через файл `.env`).
