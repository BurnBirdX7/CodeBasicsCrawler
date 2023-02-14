
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

```shell
scrapy crawl CodeBasics
```

Сбор данных с платформы CodeBasics и обновление БД

С конфигурацией по умолчанию пароль для БД можно задать через переменную окружения `DB_PASSWORD`
(или через файл `.env`).


## Конфигурация

В `config.py` нужно указать данные для подключения к БД, а также можно поменять переопределить
название сущностей 


## Вывод в файл
Чтобы помимо сохранения данных в БД сохранить собранные данные в файл, нужно добавить флаг `-o <file>`

Пример:
```shell
scrapy crawl CodeBasics -o data.json
```

Scrapy поддерживает
[различные форматы вывода](https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-format-jsonlines).
В их числе `json`, `csv` и `xml`.