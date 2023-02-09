import psycopg2
from config import Config


def table(name):
    return f'{Config.DB_SCHEMA}.{name}'


def meta_table():
    return table(Config.DB_METADATA_TABLE)


def raw_table():
    return table(Config.DB_RAW_TABLE)


def init_db():
    return psycopg2.connect(user=Config.DB_USER,
                            password=Config.DB_PASSWORD,
                            host=Config.DB_HOST,
                            port=Config.DB_PORT,
                            database=Config.DB_NAME)

