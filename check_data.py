import asyncpg
import asyncio

async def check_data():
    conn = await asyncpg.connect(user='user', password='password', database='starwars', host='127.0.0.1')
    rows = await conn.fetch('SELECT * FROM characters order by id')
    await conn.close()
    return rows

async def main():
    rows = await check_data()
    for row in rows:
        print(dict(row))

asyncio.run(main())
