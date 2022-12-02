import scrapy


# Данные по курсам:
# 1. название курса
# 1.1 название поставщика
# 2. описание,
# 2.1. ключевые скилы
# 3. программа (самая подробная)
# 4. срок (длительность)
# 5. стоимость
# 6. уровень подготовки (базовый, средний, продвинутый)
# 7. отзывы и оценка слушателей

class CourseItem(scrapy.Item):
    url = scrapy.Field()

    title = scrapy.Field()              # 1
    long_title = scrapy.Field()         # ~1

    description = scrapy.Field()        # 2
    skills = scrapy.Field()             # 2.1

    education_plan = scrapy.Field()     # 3

    estimated_duration = scrapy.Field() # 4

    cost = scrapy.Field()               # 5

    entry_level = scrapy.Field()        # 6

    reviews = scrapy.Field()            # 7
