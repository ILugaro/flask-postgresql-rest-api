import psycopg2
from decouple import config
from psycopg2 import DatabaseError


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
