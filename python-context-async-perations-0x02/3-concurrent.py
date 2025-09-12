import asyncio
import aiosqlite


async def async_fetch_users():
    connection =  aiosqlite.connect("ALX_prodev")
    cursor = connection.cursor
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    return results


async def async_fetch_older_users():
    connection =  aiosqlite.connect("ALX_prodev")
    cursor = connection.cursor
    cursor.execute("SELECT * FROM users WHERE age > 40")
    results_older = cursor.fetchall()
    return results_older


async def fetch_concurrently():
    results, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    
asyncio.run(fetch_concurrently())