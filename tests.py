import os
import hashlib
import pytest
from main import download_file

@pytest.mark.asyncio
async def test_download_file(tmp_path):
    url = 'https://gitea.radium.group/radium/project-configuration'
    file_path = os.path.join(tmp_path, 'test.txt')
    await download_file(url, file_path)
    assert os.path.exists(file_path)
    with open(file_path, 'rb') as f:
        contents = f.read()
        assert hashlib.sha256(contents).hexdigest() == 'ef495c0b28d9f781187900da7e86c441384a75a75901c8e62d7b08ccfcf29c16'
