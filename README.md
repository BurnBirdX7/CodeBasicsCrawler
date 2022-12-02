
# CodeBasics scrapper

Собирает данные о курсах с платформы [CodeBasics](https://code-basics.com/ru).

## Требования

Требует пакет `scrapy`.

## Запуск

В корне проекта запустить
```shell
scrapy crawl CodeBasics -o out.csv
```

Ключ `-o` описывает выходной файл.
Точно поддерживаются форматы CSV и JSON.

