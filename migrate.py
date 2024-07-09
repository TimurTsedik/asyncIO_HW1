import asyncpg
import asyncio

async def migrate():
    conn = await asyncpg.connect(user='user', password='password', database='starwars', host='127.0.0.1')
    await conn.execute('''
        DROP TABLE IF EXISTS characters;
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            birth_year VARCHAR(20),
            eye_color VARCHAR(50),
            films TEXT,
            gender VARCHAR(20),
            hair_color VARCHAR(50),
            height INTEGER,
            homeworld VARCHAR(100),
            mass INTEGER,
            name VARCHAR(100),
            skin_color VARCHAR(50),
            species TEXT,
            starships TEXT,
            vehicles TEXT
        )
    ''')
    await conn.close()

asyncio.run(migrate())
