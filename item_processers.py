from typing import List, Any, Dict, Tuple
from course_crawler.items import CourseItem

def duration_ru2en(dur_ru: str) -> str:
    # Always expects hours
    return dur_ru.split(' ')[0] + " hours"


class Insertable:
    def __init__(self, columns: List[str], data: List[Any]):
        self.columns = columns
        self.data = data

    def column_headers(self) -> str:
        return ', '.join([f'"{s}"' for s in self.columns])

    def column_placeholders(self) -> str:
        return ', '.join(['%s' for _ in range(len(self.columns))])

    def append(self, column: str, value: Any):
        self.columns.append(column)
        self.data.append(value)

    def request(self, table: str, additional: str = ''):
        text = f"""
        INSERT INTO {table} ({self.column_headers()})
        VALUES ({self.column_placeholders()})
        {additional}
        """

        return text

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
        duration_ru2en(item['estimated_duration']),
        levels[item['entry_level']]
    ]

    return Insertable(columns, data)


class Updatable(Insertable):
    def __init__(self, columns: List[str], data: List[Any]):
        super().__init__(columns, data)

    def append_id(self, id: int):
        self.data.append(id)

    def request(self, table: str, where = 'id = %s', additional: str = ''):
        if len(self.columns) > 1:
            OP = '('
            CL = ')'
        else:
            OP = ''
            CL = ''

        return f"""
        UPDATE {table}
        SET {OP + self.column_headers() + CL} = {OP + self.column_placeholders() + CL}
        WHERE {where}
        {additional}
        """


def updatables_from_item(item: CourseItem, id: int, levels: Dict[str, int]) -> Tuple[Updatable, Updatable]:
    meta_columns = ["duration", "level_id"]
    meta_data = [
        duration_ru2en(item['estimated_duration']),
        levels[item['entry_level']]
    ]

    meta_updatable = Updatable(meta_columns, meta_data)
    meta_updatable.append_id(id)

    raw_updatable = Updatable(['program'], [item['education_plan']])
    raw_updatable.append_id(id)

    return meta_updatable, raw_updatable
