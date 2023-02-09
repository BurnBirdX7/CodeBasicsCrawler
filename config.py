from os import getenv

class Config:
    # Connection info
    DB_HOST = 'localhost'
    DB_PORT = '49153'
    DB_USER = 'postgres'
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_NAME = 'platform'

    #
    PLATFORM_URL = 'https://code-basics.com/ru'

    # Schema and Table names
    DB_SCHEMA = 'courses'
    DB_METADATA_TABLE = 'course_metadata'
    DB_RAW_TABLE = 'course_raw'
    DB_LEVEL_TABLE = 'level'
    DB_SOURCE_TABLE = 'source'

