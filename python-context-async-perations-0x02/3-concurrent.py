# File: 3-concurrent.py

import asyncio
import aiosqlite

# ✅ async_fetch_users: fetch all users


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("[All Users]")
            for user in users:
                print(user)

# ✅ async_fetch_older_users: fetch users older than 40


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\n[Users Older Than 40]")
            for user in older_users:
                print(user)

# ✅ Run both concurrently


async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# ✅ Run entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
