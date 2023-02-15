import psycopg2
from config import Config
from item_processers import *

def table(name):
    return f'{Config.DB_SCHEMA}.{name}'

def meta_table():
    return table(Config.DB_METADATA_TABLE)

def raw_table():
    return table(Config.DB_RAW_TABLE)

def levels_table():
    return table(Config.DB_LEVEL_TABLE)

def source_table():
    return table(Config.DB_SOURCE_TABLE)

def init_db():
    return psycopg2.connect(user=Config.DB_USER,
                            password=Config.DB_PASSWORD,
                            host=Config.DB_HOST,
                            port=Config.DB_PORT,
                            database=Config.DB_NAME)

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
            print(f'DB -> platform_id={packed_id[0]}')
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
    insertable = Insertable(levels_table(), ['text'], [level])
    with db.cursor() as crs:
        crs.execute(insertable.request(), insertable.data)
        db.commit()


def get_levels_ids(db, nested: bool = False) -> Dict[str, int]:
    select_text = f"""
    SELECT id, text
    FROM {levels_table()}
    WHERE text = %s or text = %s
    """

    wanted_levels = [Config.LEVEL_BASIC, Config.LEVEL_MIDDLE]

    with db.cursor() as crs:
        crs.execute(select_text, wanted_levels)
        rows = crs.fetchall()

        dic = {}
        for id, text in rows:
            print(f'DB -> [entry level] {id=}, {text=}')
            if text == Config.LEVEL_BASIC:
                dic['Basic'] = id
            elif text == Config.LEVEL_MIDDLE:
                dic['Middle'] = id
            else:
                raise RuntimeError(f'Cannot recognize role [{id=}, {text=}]')

        if len(dic) < 2:
            if nested:
                raise RuntimeError('Cannot acquire entry level information from database')

            for level in wanted_levels:
                if level not in dic:
                    insert_level(db, level)

            return get_levels_ids(db, True)

        return dic
