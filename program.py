"""Module for downloading files from a URL and calculating their SHA256 hash."""

import asyncio
import hashlib
import os

import aiohttp


async def download_file(url: str, path: str) -> None:
    """Download a file from a given URL and save it to a specified path."""
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as resp:
            if resp.status == 200:
                async with session.get(url) as response:
                    with open(path, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)


async def main() -> None:
    """Download files from a given URL, save them to temporary directory, and calculate their SHA256 hash."""
    url = 'https://gitea.radium.group/radium/project-configuration'
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    tasks = []
    for i in range(3):
        file_name = f'file_{i}.txt'
        file_path = os.path.join(temp_dir, file_name)
        task = asyncio.create_task(download_file(url, file_path))
        tasks.append(task)
    await asyncio.gather(*tasks)
    hashes = []
    for i in range(3):
        file_name = f'file_{i}.txt'
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path, 'rb') as f:
            file_contents = f.read()
            hash_object = hashlib.sha256(file_contents)
            hash_hex = hash_object.hexdigest()
            hashes.append(hash_hex)
    print(hashes)


if __name__ == '__main__':
    asyncio.run(main())
