from os import getenv

class Config:
    DB_HOST = 'localhost'
    DB_PORT = '49153'
    DB_USER = 'postgres'
    DB_PASSWORD = getenv('DB_PASSWORD')
    DB_NAME = 'edu_courses'

    DB_COURSE_TABLE = 'course'
    DB_SOURCE_TABLE = 'platform'

    PLATFORM_URL = 'https://code-basics.com/ru'
