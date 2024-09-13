import base64
import os
import tempfile

import requests
from model import AudioBase64, AudioUrl


def base64_to_tempfile(base64_data: AudioBase64) -> str:
    """
    Decode base64 data and write it to a temporary file.
    Returns the path to the temporary file.
    """
    # Decode the base64 data to bytes
    audio_data = base64.b64decode(base64_data.base64_bytes)

    # Create a temporary file and write the decoded data
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    with open(temp_file.name, 'wb') as file:
        file.write(audio_data)

    # Confirm the file is written and exists
    assert os.path.exists(temp_file.name)

    return temp_file.name

def download_file(url: AudioUrl) -> str:
    """
    Download a file from a URL to a temporary file and return its path.
    """
    response = requests.get(url.url)
    if response.status_code != 200:
        raise requests.exceptions.RequestException("Failed to download file from URL")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name