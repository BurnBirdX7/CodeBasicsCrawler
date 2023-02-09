import re
from typing import List, Any, Dict, Tuple

from course_crawler.items import CourseItem


class Insertable:
    def __init__(self, columns: List[str], data: List[Any]):
        self.columns = columns
        self.data = data

    def columns_str(self) -> str:
        return ', '.join([f'"{s}"' for s in self.columns])

    def placeholders(self) -> str:
        return ', '.join(['%s' for _ in range(len(self.columns))])

    def append(self, column: str, value: Any):
        self.columns.append(column)
        self.data.append(value)


def insertable_raw_from_item(item: CourseItem) -> Insertable:
    columns = ['title', 'section_title', 'description', 'program']

    data = [
        item[key] for key in (
            "title",
            "long_title",
            "description",
            "education_plan"
        )
    ]

    return Insertable(columns, data)


def insertable_meta_from_item(item: CourseItem, levels: Dict[str, int]) -> Insertable:
    columns = ['url', 'duration', 'level_id']

    data = [
        item['url'],
        re.search(r'\d+', item.estimated_duration),
        levels[item['entry_level']]
    ]

    return Insertable(columns, data)


class Updatable(Insertable):
    def __init__(self, columns: List[str], data: List[Any]):
        super().__init__(columns, data)

    def append_id(self, id: int):
        self.data.append(id)


def updatables_from_item(item: CourseItem, id: int, levels: Dict[str, int]) -> Tuple[Updatable, Updatable]:
    meta_columns = ["duration", "level_id"]
    meta_data = [
        re.search(r'\d+', item.estimated_duration),
        levels[item['entry_level']]
    ]

    meta_updatable = Updatable(meta_columns, meta_data)
    meta_updatable.append_id(id)

    raw_updatable = Updatable(['program'], [item['education_plan']])
    raw_updatable.append_id(id)

    return meta_updatable, raw_updatable
