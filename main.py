from dotenv import load_dotenv
load_dotenv()

from scrapy.crawler import CrawlerProcess
from course_crawler.spiders.CodeBasics import CourseSpider

import psycopg2
from config import Config


def crawl(callback):
    collection = []

    process = CrawlerProcess()
    process.crawl(CourseSpider, callback)
    process.start()

    return collection

def init_db():
    return psycopg2.connect(user=Config.DB_USER,
                            password=Config.DB_PASSWORD,
                            host=Config.DB_HOST,
                            port=Config.DB_PORT,
                            database=Config.DB_NAME)


def get_platform_id(db):

    select_text = f"""
    SELECT id
    FROM {Config.DB_SOURCE_TABLE}
    WHERE url = %s
    """

    with db.cursor() as crs:
        crs.execute(select_text, [Config.PLATFORM_URL])
        lst = crs.fetchone()
        print(lst[0])
        return lst[0]

scanned = 0
updated = 0
inserted = 0

def push_item(db, platform_id, item):
    insertable = [
        item[key] for key in ("url",
                              "title",
                              "long_title",

                              "description",
                              "education_plan",
                              "estimated_duration",

                              "entry_level") # cost, platform
    ]

    insertable.append(platform_id)

    with db.cursor() as crs:
        insert_text = f"""
        INSERT INTO {Config.DB_COURSE_TABLE} (
            url, subject, title,
            description, plan, estimated_duration,
            entry_level, cost, platform_id
            )
        VALUES (%s, %s, %s,
                %s, %s, %s,
                %s, 0,  %s)
        """

        crs.execute(insert_text, insertable)
        db.commit()

    global inserted
    inserted += 1


def update_item(db, course_id, item):
    updatable = [item[key] for key in ("estimated_duration", "entry_level", "education_plan")]

    updatable.append(course_id)

    update_text = f"""
                UPDATE {Config.DB_COURSE_TABLE}
                SET (estimated_duration, entry_level, plan) = (%s, %s, %s)
                WHERE id = %s
                """

    with db.cursor() as crs:
        crs.execute(update_text, updatable)
        db.commit()

    global updated
    updated += 1

def process_item(db, platform_id, item):
    select_text = f"""
        SELECT id, estimated_duration, description, entry_level, plan
        FROM {Config.DB_COURSE_TABLE}
        WHERE url = %s
        """

    with db.cursor() as crs:
        crs.execute(select_text, [item["url"]])
        course = crs.fetchone()

    global scanned
    scanned += 1

    if course is None:
        push_item(db, platform_id, item)
        return

    course_id, duration, description, entry_level, plan = course

    # TODO: Make more general
    if duration != item["estimated_duration"]  or \
            description != item["description"] or \
            entry_level != item["entry_level"] or \
            plan != item["education_plan"]:
        update_item(db, course_id, item)


def main():
    db = init_db()
    platform_id = get_platform_id(db)
    crawl(lambda item: process_item(db, platform_id, item))
    db.close()

    global inserted, updated, scanned

    print(f'{inserted=}')
    print(f'{updated=}')
    print(f'{scanned=}')

if __name__ == '__main__':
    main()
