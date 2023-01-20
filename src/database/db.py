import psycopg2
from psycopg2 import DatabaseError
from decouple import config


def get_connection():
    try:
        return psycopg2.connect(
            host=config('PGSQL_HOST'),
            user=config('POSTGRES_USER'),
            password=config('POSTGRES_PASSWORD'),
            database=config('POSTGRES_DB'),
        )
    except DatabaseError as ex:
        raise ex
