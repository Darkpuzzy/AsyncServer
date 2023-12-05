import os
from passlib.hash import bcrypt

from dotenv import load_dotenv

DEBUG = True

load_dotenv()

DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ["POSTGRES_PORT"]
DB_NAME = os.environ["POSTGRES_DB_NAME"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASS = os.environ["POSTGRES_PASSWORD"]

admins = os.environ["SUPERUSER"]
SERVER_PASS = os.environ["SERVER_PASSWORD"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_SEED = os.environ["SECRET_SEED"]

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

CONVENTION = {
    'all_column_names': lambda constraint, table: '_'.join([column.name for column in constraint.columns.values()]),
    'ix'              : 'ix__%(table_name)s__%(all_column_names)s',
    'uq'              : 'uq__%(table_name)s__%(all_column_names)s',
    'ck'              : 'ck__%(table_name)s__%(constraint_name)s',
    'fk'              : 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk'              : 'pk__%(table_name)s'
}

