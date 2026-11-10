import asyncio

import aiosqlite

DB_PATH = "chef.db"


async def get_db():
    return await aiosqlite.connect(DB_PATH)


async def dbcreate_tables():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'en'
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER PRIMARY KEY,
                recipes TEXT,

                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()



async def dbadd_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
        """, (user_id,))

        await db.commit()



async def dbupdate_user_language(user_id: int, language: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (language, user_id)
        )

        await db.commit()


async def dbget_user_language(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT language FROM users WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            result = await cursor.fetchone()

        return result[0] if result else "en"


async def main():
    await dbcreate_tables()

if __name__ == "__main__":
    asyncio.run(main())

