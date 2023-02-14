from os import getenv
import dotenv
dotenv.load_dotenv()

class Config:
    # DB connection info
    DB_HOST = 'localhost'
    DB_USER = 'postgres'
    DB_PORT = getenv('DB_PORT')
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_NAME = getenv('DB_NAME')

    # Defines how platform is represented in the DB
    PLATFORM_URL = 'https://code-basics.com/ru'

    # Schema and Table names
    DB_SCHEMA = 'courses'
    DB_METADATA_TABLE = 'course_metadata'
    DB_RAW_TABLE = 'course_raw'
    DB_LEVEL_TABLE = 'level'
    DB_SOURCE_TABLE = 'source'

    # Entry levels' names in the database (Level Table)
    LEVEL_BASIC = 'CodeBasics_Basic'
    LEVEL_MIDDLE = 'CodeBasics_Middle'
