from dotenv import load_dotenv
load_dotenv()

from scrapy.crawler import CrawlerProcess
from course_crawler.spiders.CodeBasics import CourseSpider

from db_helpers import *
from item_processers import *
from typing import Dict

def crawl(callback):
    collection = []

    process = CrawlerProcess()
    process.crawl(CourseSpider, callback)
    process.start()

    return collection


def get_platform_id(db):
    SELECT_TEXT = f"""
    SELECT id
    FROM {table(Config.DB_SOURCE_TABLE)}
    WHERE url = %s
    """

    INSERT_TEXT = f"""
    INSERT INTO {table(Config.DB_SOURCE_TABLE)} (url)
    VALUES (%s)
    RETURNING id
    """

    with db.cursor() as crs:
        crs.execute(SELECT_TEXT, [Config.PLATFORM_URL])
        packed_id = crs.fetchone()

        if packed_id is not None:
            print('platform id:', packed_id[0])
            return packed_id[0]

    # If platform wasn't found - insert it
    with db.cursor() as crs:
        crs.execute(INSERT_TEXT, (Config.PLATFORM_URL,))
        packed_id = crs.fetchone()
        if packed_id is not None:
            db.commit()
            return packed_id[0]

        raise RuntimeError(f'Cannot acquire ID of the platform with \'{Config.PLATFORM_URL}\' url')


def insert_level(db, level: str):
    insert_text = f"""
    INSERT INTO {Config.DB_SCHEMA}.{Config.DB_LEVEL_TABLE} (text)
    VALUES (%s)
    ON CONFLICT DO NOTHING
    """

    with db.cursor() as crs:
        crs.execute(insert_text, (level,))
        db.commit()


def get_levels_ids(db, nested: bool = False) -> Dict[str, int]:
    print('levels:')
    select_text = f"""
    SELECT id, text
    FROM {Config.DB_SCHEMA}.{Config.DB_LEVEL_TABLE}
    WHERE text = %s or text = %s
    """

    wanted_levels = [Config.LEVEL_BASIC, Config.LEVEL_MIDDLE]

    with db.cursor() as crs:
        crs.execute(select_text, wanted_levels)
        rows = crs.fetchall()

        dic = {}
        for id, text in rows:
            print(f'{id=}, {text=}')
            if text == Config.LEVEL_BASIC:
                dic['Basic'] = id
            else:
                dic['Middle'] = id

        if len(dic) < 2:
            if nested:
                raise RuntimeError('Cannot acquire entry level information from database')

            for level in wanted_levels:
                if level not in dic:
                    insert_level(db, level)

            return get_levels_ids(db, True)

        return dic


scanned = 0
updated = 0
inserted = 0


def insert_item(db, platform_id: int, levels: Dict, item: CourseItem):
    raw_insertable = insertable_raw_from_item(item)

    meta_insertable = insertable_meta_from_item(item, levels)
    meta_insertable.append('source_id', platform_id)

    with db.cursor() as crs:
        meta_insert_text = f"""
            INSERT INTO {meta_table()} ({meta_insertable.columns_str()})
            VALUES ({meta_insertable.placeholders()})
            RETURNING id
            """

        crs.execute(meta_insert_text, meta_insertable.data)
        packed_id = crs.fetchone()
        if packed_id is None:
            raise RuntimeError('Cannot insert course into meta-information table')

        raw_insertable.append('course_id', packed_id[0])
        raw_insert_text = f"""
            INSERT INTO {raw_table()} ({raw_insertable.columns_str()})
            VALUES ({raw_insertable.placeholders()})
            """

        crs.execute(raw_insert_text, raw_insertable.data)
        db.commit()

    global inserted
    inserted += 1


def update_item(db, course_id: int, levels: Dict[str, int], item: CourseItem):
    meta_upd, raw_upd = updatables_from_item(item, course_id, levels)

    meta_update_text = f"""
        UPDATE {meta_table()}
        SET ({meta_upd.columns_str()}) = ({meta_upd.placeholders()})
        WHERE id = %s
        """

    raw_update_text = f"""
        UPDATE {raw_table()}
        SET {raw_upd.columns_str()} = {raw_upd.placeholders()}
        WHERE course_id = %s
        """

    with db.cursor() as crs:
        crs.execute(meta_update_text, meta_upd.data)
        crs.execute(raw_update_text, raw_upd.data)
        db.commit()

    global updated
    updated += 1


def process_item(db, platform_id: int, levels: Dict[str, int], item: CourseItem):
    select_text = f"""
        SELECT m.id, m.duration, r.title, r.description, level_id, program
        FROM {meta_table()} m
        JOIN {raw_table()} r ON r.course_id = m.id 
        WHERE url = %s
        """

    with db.cursor() as crs:
        crs.execute(select_text, [item["url"]])
        course = crs.fetchone()

    global scanned
    scanned += 1

    if course is None:
        return insert_item(db, platform_id, levels, item)

    course_id, duration, title, description, level_id, program = course
    print(f'{course_id=}, {duration=}, {title=}, {program=}')
    if      duration    != item["estimated_duration"]   or \
            description != item["description"]          or \
            level_id    != levels[item["entry_level"]]  or \
            program     != item["education_plan"]:
        update_item(db, course_id, levels, item)


def main():
    db = init_db()
    platform_id = get_platform_id(db)
    levels = get_levels_ids(db)
    crawl(lambda item: process_item(db, platform_id, levels, item))
    db.close()

    global inserted, updated, scanned

    print(f'{inserted=}')
    print(f'{updated=}')
    print(f'{scanned=}')


if __name__ == '__main__':
    main()
