# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from db_helpers import *
from typing import Dict

class CodeBasicsPipeline:

    def log(self, text):
        print(f"\t>>>> PIPLINE: {text}")

    def __init__(self):
        self.db:          psycopg2.connection   | None = None
        self.platform_id: int                   | None = None
        self.levels:      Dict[str, int]        | None = None

        self.scanned:  int = 0
        self.inserted: int = 0
        self.updated:  int = 0

    def open_spider(self, spider):
        self.db = init_db()
        self.platform_id = get_platform_id(self.db)
        self.levels = get_levels_ids(self.db)
        self.log("DB connection's initialized")

    def close_spider(self, spider):
        self.db.close()
        self.log("DB connection's closed")
        self.log(f"Scanned: {self.scanned},"
                 f"Inserted: {self.inserted},"
                 f"Updated: {self.updated}")

    def process_item(self, item, spider):
        self.log("Item processed")
        self._process_item(item)
        self.scanned += 1
        return item

    def insert_item(self, item: CourseItem):
        raw_insertable = insertable_raw_from_item(item)

        meta_insertable = insertable_meta_from_item(item, self.levels)
        meta_insertable.append('source_id', self.platform_id)

        with self.db.cursor() as crs:
            meta_insert_text = meta_insertable.request(meta_table(), "RETURNING id")
            crs.execute(meta_insert_text, meta_insertable.data)

            packed_id = crs.fetchone()
            if packed_id is None:
                raise RuntimeError('Cannot insert course into meta-information table')

            raw_insertable.append('course_id', packed_id[0])

            raw_insert_text = raw_insertable.request(raw_table())
            crs.execute(raw_insert_text, raw_insertable.data)
            self.db.commit()

        self.inserted += 1

    def update_item(self, course_id: int, item: CourseItem):
        meta_upd, raw_upd = updatables_from_item(item, course_id, self.levels)

        meta_update_text = meta_upd.request(meta_table())
        raw_update_text = raw_upd.request(raw_table(), "course_id = %s")

        with self.db.cursor() as crs:
            crs.execute(meta_update_text, meta_upd.data)
            crs.execute(raw_update_text, raw_upd.data)
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
            return self.insert_item(item)

        course_id, duration, title, description, level_id, program = course
        print(f'{course_id=}, {duration=}, {title=}, {program=}')
        if duration != item["estimated_duration"] or \
                description != item["description"] or \
                level_id != self.levels[item["entry_level"]] or \
                program != item["education_plan"]:
            self.update_item(course_id, item)

