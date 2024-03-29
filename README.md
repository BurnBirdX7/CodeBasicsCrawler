
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

С конфигурацией по умолчанию пароль, порт и имя БД задаются
через переменные окружения `DB_PASSWORD`, `DB_PORT` и `DB_NAME` соответственно
(или через файл `.env`).

## Конфигурация

В `config.py` нужно указать данные для подключения к БД, а также можно поменять переопределить
название сущностей.

## Вывод в файл
Чтобы помимо сохранения данных в БД сохранить собранные данные в файл, нужно добавить флаг `-o <file>`

Пример:
```shell
scrapy crawl CodeBasics -o data.json
```

Scrapy поддерживает
[различные форматы вывода](https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-format-jsonlines).
В их числе `json`, `csv` и `xml`.

## Детали

### Порог входа

На CodeBasics есть курсы двух видов: "... с нуля" и "... как второй язык".
Эти две категории по умолчанию записываются в БД как `CodeBasics_Basic` и `CodeBasics_Middle` соответственно.
Эти названия можно поменять на любые другие в `config.py`.

Если эти уровни входа отсутствуют в БД, то они будут добавлены в таблицу `DB_LEVELS`.
