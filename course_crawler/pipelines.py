# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from db_helpers import *
from typing import Dict

class CodeBasicsPipeline:

    def log(self, text, no_new_line:bool=False):
        print(f" > PIPELINE > : {text}", end=(' ' if no_new_line else '\n'))

    def __init__(self):
        self.db:          psycopg2.connection   | None = None
        self.platform_id: int                   | None = None
        self.levels:      Dict[str, int]        | None = None

        self.scanned:  int = 0
        self.inserted: int = 0
        self.updated:  int = 0
        self.uptodate: int = 0

    def open_spider(self, spider):
        self.db = init_db()
        self.log("DB connection's initialized")
        self.platform_id = get_platform_id(self.db)
        self.levels = get_levels_ids(self.db)

    def close_spider(self, spider):
        self.db.close()
        self.log("DB connection's closed")
        self.log(f"Scanned: {self.scanned},"
                 f"Inserted: {self.inserted},"
                 f"Updated: {self.updated}, "
                 f"Up to date: {self.uptodate}")

    def process_item(self, item, spider):
        self.log("Processing item...", True)
        self._process_item(item)
        self.scanned += 1
        return item

    def insert_item(self, item: CourseItem):
        raw_insertable = insertable_raw_from_item(item, raw_table())

        meta_insertable = insertable_meta_from_item(item, meta_table(), self.levels)
        meta_insertable.append_column('source_id', self.platform_id)
        meta_insertable.append_additional("RETURNING id")

        with self.db.cursor() as crs:
            crs.execute(meta_insertable.request(), meta_insertable.data)

            packed_id = crs.fetchone()
            if packed_id is None:
                raise RuntimeError(f'Cannot insert course into meta-information table [{meta_table()}]')

            raw_insertable.append_column('course_id', packed_id[0])

            raw_insert_text = raw_insertable.request()
            crs.execute(raw_insert_text, raw_insertable.data)
            self.db.commit()

        self.inserted += 1

    def update_item(self, course_id: int, item: CourseItem):
        meta_upd, raw_upd = updatables_from_item(item, meta_table(), raw_table(), course_id, self.levels)

        with self.db.cursor() as crs:
            crs.execute(meta_upd.request(), meta_upd.data)
            crs.execute(raw_upd.request(), raw_upd.data)
            self.db.commit()

        self.updated += 1

    def _process_item(self, item: CourseItem):
        select_text = f"""
            SELECT m.id, m.duration, r.title, r.description, level_id, program
            FROM {meta_table()} m
            JOIN {raw_table()} r ON r.course_id = m.id 
            WHERE url = %s
            """

        with self.db.cursor() as crs:
            crs.execute(select_text, [item["url"]])
            course = crs.fetchone()

        if course is None:
            print(f"Inserting... [title={item['title']}, url={item['url']}]")
            return self.insert_item(item)

        course_id, duration, title, description, level_id, program = course
        duration: datetime.timedelta
        duration = f'{int(duration.total_seconds() / 3600)} hours'
        if duration != item["estimated_duration"] or \
                description != item["description"] or \
                level_id != self.levels[item["entry_level"]] or \
                program != item["education_plan"]:
            self.update_item(course_id, item)
            print(f"Updating... [{course_id=}, {title=}]")
        else:
            print('Up to date')
            self.uptodate += 1

