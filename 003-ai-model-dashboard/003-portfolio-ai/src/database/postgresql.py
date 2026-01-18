from dotenv import load_dotenv
import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

@contextmanager
def get_pg_db():
    """
    PostgreSQL 연결을 생성하고 사용 후 안전하게 닫습니다.
    """
    db = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DB,
        sslmode="require"
    )

    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_pg_cursor():
    with get_pg_db() as db:
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
            db.commit()