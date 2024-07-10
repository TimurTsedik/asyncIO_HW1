import aiohttp
import asyncio
import asyncpg

BASE_URL = 'https://swapi.dev/api/people/'

async def fetch_character(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            print(f"Successfully fetched {url}")
            return await response.json()
        else:
            print(f"Failed to fetch {url}: {response.status}")
            return None

async def fetch_name(session, url, key_name: str):
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data.get(key_name, 'Unknown')
        else:
            print(f"Failed to fetch {url}: {response.status}")
            return 'Unknown'

async def insert_character(pool, character, films, species, starships, vehicles):
    async with pool.acquire() as conn:
        await conn.execute('''
            INSERT INTO characters (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        ''', character['birth_year'], character['eye_color'], films, character['gender'], character['hair_color'],
            int(character['height']) if character['height'].isdigit() else None,
            character['homeworld'], int(character['mass']) if character['mass'].isdigit() else None,
            character['name'], character['skin_color'],
            species, starships, vehicles)

async def main():
    pool = await asyncpg.create_pool(user='user', password='password', database='starwars', host='127.0.0.1')
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as response:
            if response.status == 200:
                data = await response.json()
                tasks = []
                for i in range(1, data['count'] + 1):
                    tasks.append(fetch_character(session, f"{BASE_URL}{i}/"))
                characters = await asyncio.gather(*tasks)

                insert_tasks = []
                for character in characters:
                    if character:
                        films = ', '.join([await fetch_name(session, film, 'title') for film in character['films']])
                        species = ', '.join([await fetch_name(session, specie, 'name') for specie in character['species']])
                        starships = ', '.join([await fetch_name(session, starship, 'name') for starship in character['starships']])
                        vehicles = ', '.join([await fetch_name(session, vehicle, 'name') for vehicle in character['vehicles']])
                        insert_tasks.append(insert_character(pool, character, films, species, starships, vehicles))

                await asyncio.gather(*insert_tasks)
                print("Data loaded successfully!")
            else:
                print(f"Failed to fetch initial data: {response.status}")

    await pool.close()

asyncio.run(main())
