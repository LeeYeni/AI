from src.database.postgresql import get_pg_cursor

async def save_guestbook_message(nickname: str, context: str):
    """
    방명록을 저장합니다.
    """
    with get_pg_cursor() as cur:
        query = """
        INSERT INTO guestbook (nickname, context)
        VALUES (%s, %s)
        """
        cur.execute(query, (nickname, context))

async def get_guestbook_messages():
    """
    방명록 목록을 가져옵니다.
    """
    with get_pg_cursor() as cur:
        query = """
        SELECT * FROM (
            SELECT id, nickname, context, created_at
            FROM guestbook
            ORDER BY created_at DESC
            LIMIT 50
        ) AS subquery
        ORDER BY created_at ASC;
        """
        cur.execute(query)
        return cur.fetchall()