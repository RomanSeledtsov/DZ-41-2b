import sqlite3

import aiosqlite
from database import sql_quaries


class AsyncDatabase:
    def __init__(self, db_path='db.sqlite3'):
        self.db_path = db_path

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_quaries.CREATE_USER_TABLE_QUERY)
            await db.execute(sql_quaries.CREATE_PROFILE_TABLE_QUERY)
            await db.execute(sql_quaries.CREATE_LIKE_DISLIKE_TABLE_QUERY)
            await db.execute(sql_quaries.CREATE_TABLE_REFERENCE_QUERY)
            await db.execute(sql_quaries.CREATE_DONATE_TRANSACTIONS_TABLE_QUERY)
            await db.execute(sql_quaries.CREATE_WALLET_TRANSACTIONS_TABLE_QUERY)
            try:
                await db.execute(sql_quaries.ALTER_TABLE_USER_QUERY_V1)
                await db.execute(sql_quaries.ALTER_TABLE_USER_QUERY_V2)
            except sqlite3.OperationalError:
                pass

            await db.commit()
            print("Database connected successfully")

    async def execute_query(self, query, params=None, fetch="none"):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params or ())

            if fetch == "none":
                await db.commit()
                return
            elif fetch == "all":
                data = await cursor.fetchall()
                return [dict(row) for row in data] if data else []
            elif fetch == 'one':
                data = await cursor.fetchone()
                return dict(data) if data else None
