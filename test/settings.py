import os

# Connection params

DIALECT = 'postgresql'
DRIVER = 'psycopg2'
USERNAME = 'postgres'
PASSWORD = os.environ.get('FANTALYTIX_DB_PASSWORD', '')
HOST = 'localhost'
PORT = '5432'
DATABASE = 'fantalytix-test'
CONNECTION = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'.format(
    dialect = DIALECT,
    driver = DRIVER,
    username = USERNAME,
    password = PASSWORD,
    host = HOST,
    port = PORT,
    database = DATABASE
    )
