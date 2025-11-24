import psycopg2
from psycopg2.extras import RealDictCursor

DB_PARAMS = {
    "dbname": "cap_db",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS, cursor_factory=RealDictCursor)
