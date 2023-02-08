
# CodeBasics scrapper

Собирает данные о курсах с платформы [CodeBasics](https://code-basics.com/ru).

## Требования

Python-пакеты:
 * `scrapy` - Скраппер
 * `psycopg2` - PostgreSQL драйвер
 * `dotenv` - Загрузка переменных окржения из `.env` файла

```shell
python3 -m pip install scrapy psycopg2 dotenv
```

## Запуск

В корне проекта запустить
```shell
scrapy crawl CodeBasics -o out.csv
```

Ключ `-o` описывает выходной файл.
Точно поддерживаются форматы CSV и JSON.

