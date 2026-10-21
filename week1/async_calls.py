import asyncio
import time
import httpx

URLS = [
    "https://api.github.com/users/lakshaysharma0703-droid",
    "https://api.github.com/repos/python/cpython",
    "https://httpbin.org/delay/2",              # deliberately takes 2 seconds
]

async def fetch(client: httpx.AsyncClient, url:str) -> int:
    response = await client.get(url,timeout=10)
    print(f"{response.status_code} {url}")
    return response.status_code

async def run_sequential():
    async with httpx.AsyncClient() as client:
        for url in URLS:
            await fetch(client,url)

async def run_concurrent():
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client,url) for url in URLS]
        results = await asyncio.gather(*tasks)
        print(f"Status code {results}")

async def main():
    start = time.perf_counter()
    await run_sequential()
    print(f"Sequential took {time.perf_counter() - start:.2f}s\n")

    start = time.perf_counter()
    await run_concurrent()
    print(f"concurrent took {time.perf_counter() - start:.2f}s\n")

asyncio.run(main())