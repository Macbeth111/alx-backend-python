# File: 3-concurrent.py

import asyncio
import aiosqlite

# ✅ async_fetch_users: fetch all users


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users  # ⬅️ Required by ALX checker

# ✅ async_fetch_older_users: fetch users older than 40


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users  # ⬅️ Required by ALX checker

# ✅ Run both concurrently


async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("[All Users]")
    for user in all_users:
        print(user)

    print("\n[Users Older Than 40]")
    for user in older_users:
        print(user)

# ✅ Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
