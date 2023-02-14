from typing import List, Any, Dict, Tuple
from course_crawler.items import CourseItem


class Insertable:
    def __init__(self, table: str, columns: List[str], data: List[Any]):
        self.columns = columns
        self.data = data
        self.table = table
        self.additional = ''

    def column_headers(self) -> str:
        return ', '.join([f'"{s}"' for s in self.columns])

    def column_placeholders(self) -> str:
        return ', '.join(['%s' for _ in range(len(self.columns))])

    def append_column(self, column: str, value: Any):
        self.columns.append(column)
        self.data.append(value)

    def append_additional(self, additional: str):
        self.additional += additional

    def request(self):
        text = f"""
        INSERT INTO {self.table} ({self.column_headers()})
        VALUES ({self.column_placeholders()})
        {self.additional}
        """

        return text

class Updatable(Insertable):
    def __init__(self, table:str, columns: List[str], data: List[Any]):
        super().__init__(table, columns, data)
        self.where = ''

    def append_id(self, id: int):
        self.data.append(id)

    def where_(self, condition: str):
        self.where = condition
        return self

    def or_(self, condition: str):
        self.where += f' OR {condition}'
        return self

    def and_(self, condition: str):
        self.where += f' AND {condition}'

    def request(self):
        if len(self.columns) > 1:
            OP = '('
            CL = ')'
        else:
            OP = ''
            CL = ''

        return f"""
        UPDATE {self.table}
        SET {OP + self.column_headers() + CL} = {OP + self.column_placeholders() + CL}
        WHERE {self.where}
        {self.additional}
        """


# Function helpers:

# Insertable:

def insertable_raw_from_item(item: CourseItem, table: str) -> Insertable:
    columns = ['title', 'section_title', 'description', 'program']

    data = [
        item[key] for key in (
            "title",
            "long_title",
            "description",
            "education_plan"
        )
    ]

    return Insertable(table, columns, data)


def insertable_meta_from_item(item: CourseItem, table:str, levels: Dict[str, int]) -> Insertable:
    columns = ['url', 'duration', 'level_id']

    data = [
        item['url'],
        item['estimated_duration'],
        levels[item['entry_level']]
    ]

    return Insertable(table, columns, data)

# Updatable

def updatables_from_item(item: CourseItem, meta_table: str, raw_table: str, id: int, levels: Dict[str, int]) -> Tuple[Updatable, Updatable]:
    meta_columns = ["duration", "level_id"]
    meta_data = [
        item['estimated_duration'],
        levels[item['entry_level']]
    ]

    meta_updatable = Updatable(meta_table, meta_columns, meta_data)
    meta_updatable.where_("id = %s")
    meta_updatable.append_id(id)

    raw_updatable = Updatable(raw_table, ['program'], [item['education_plan']])
    raw_updatable.where_("course_id = %s")
    raw_updatable.append_id(id)

    return meta_updatable, raw_updatable
