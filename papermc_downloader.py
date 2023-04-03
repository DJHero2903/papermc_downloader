#!/usr/bin/env python3

"""
A python script to download a selected version and build of paper using the papermc.io API v2.

Copyright (C) 2023  DJHero2903

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import requests
from tqdm import tqdm


def get_version(api_base: str) -> str:
    """
    Returns a chosen version of paper that are available for download.
    """
    request = requests.get(
        url=f"{api_base}/projects/paper", timeout=60, allow_redirects=True
    )
    data_list = json.loads(request.text).get("versions")
    data_str = " ".join(map(str, data_list))
    print(data_str)
    chosen_version = str(input("\nChoose one of the above versions to download. "))

    while chosen_version not in data_list:
        print("\n", data_str)
        chosen_version = str(input("\nChoose one of the above versions to download. "))

    return chosen_version


def get_build(api_base: str, version: str) -> int:
    """
    Returns the selected build for a given version of papermc that are available for download.
    """

    request = requests.get(
        url=f"{api_base}/projects/paper/versions/{version}",
        timeout=60,
        allow_redirects=True,
    )
    data_list = json.loads(request.text).get("builds")
    data_str = " ".join(map(str, data_list))
    print(data_str)
    chosen_build = int(input("\nChoose one of the above builds to download. "))

    while chosen_build not in data_list:
        print("\n", data_str)
        chosen_build = int(input("\nChoose one of the above builds to download. "))

    return chosen_build


def download_jar(url: str, file_name: str, chunk_size=1024):
    """
    Download the selected papermc jar.
    Source: https://gist.github.com/yanqd0/c13ed29e29432e3cf3e7c38467f42f51

    Changes that I have made to the source:
    1. Change function name from 'download' to 'download_jar',
    2. Added a timeout to the request,
    3. Rename 'resp' to 'request',
    3. Rename 'fname' to 'file_name',
    4. Rename 'bar' to 'progress_bar'.
    """
    request = requests.get(url, stream=True, timeout=60)
    total = int(request.headers.get("content-length", 0))
    with open(file_name, "wb") as file, tqdm(
        desc=file_name,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in request.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            progress_bar.update(size)


if __name__ == "__main__":
    API_BASE = "https://api.papermc.io/v2/"

    VERSION = get_version(api_base=API_BASE)
    BUILD = get_build(api_base=API_BASE, version=VERSION)
    JAR_FILE = f"paper-{VERSION}-{BUILD}.jar"

    DOWNLOAD_URL = f"{API_BASE}/projects/paper/versions/{VERSION}/builds/{BUILD}/downloads/{JAR_FILE}"

    print(f"\nDownloading {JAR_FILE}\n")
    download_jar(url=DOWNLOAD_URL, file_name=JAR_FILE)
    print("\nDownload complete!")
