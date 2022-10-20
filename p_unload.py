from p_load import recording
import aiohttp
import time
import asyncio
from more_itertools import chunked

concurrency = 10

async def call_api(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        if response.status == 200:

            response_json = await response.json()
            return response_json
        elif response.status == 500:
            pass

async def main():
    async with aiohttp.ClientSession() as session:
        count = await call_api((f'https://swapi.dev/api/people/'), session)
        data = (
            call_api((f'https://swapi.dev/api/people/{id}'), session)
            for id in range(1, count['count'])
        )

        for data_chunk in chunked(data, concurrency):
            tasks = []
            for data in data_chunk:
                task = asyncio.create_task(data)
                tasks.append(task)
            for task in tasks:
                data = await task
                asyncio.create_task(recording(data))


if __name__ == '__main__':
    asyncio.run(main())


