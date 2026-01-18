from dotenv import load_dotenv
import os
import pymysql
from contextlib import contextmanager

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

@contextmanager  # 'with'문에서 사용하기 위함
def get_mysql_db():
    """
    MySQL 연결을 생성하고 사용 후 안전하게 닫습니다.
    """
    db = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리 형태로 받기 위함
    )

    try:
        yield db
    finally:
        db.close()