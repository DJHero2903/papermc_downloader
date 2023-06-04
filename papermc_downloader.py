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
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt, Confirm
from rich.table import Table


def get_version(api_base: str) -> str:
    """
    Returns a chosen version of paper that are available for download.
    """
    request = requests.get(
        url=f"{api_base}/projects/paper",
        timeout=60,
        allow_redirects=True,
    )
    table = Table()
    table.add_column("Available versions", style="magenta")

    data_list = json.loads(request.text).get("versions")
    for i in data_list:
        if i != data_list[-1]:
            table.add_row(i)
        else:
            table.add_row(i, style="cyan")
    console.print(table)

    chosen_version = Prompt.ask(
        "Choose a version of paper",
        choices=data_list,
        show_choices=False,
        default=data_list[-1],
    )

    return chosen_version


def get_build(api_base: str, version: str) -> str:
    """
    Returns the selected build for a given version of papermc that are available for download.
    """
    request = requests.get(
        url=f"{api_base}/projects/paper/versions/{version}",
        timeout=60,
        allow_redirects=True,
    )

    table = Table()
    table.add_column("Available builds", style="magenta")

    data_list = json.loads(request.text).get("builds")
    for build_number in data_list:
        if build_number != data_list[-1]:
            table.add_row(str(build_number))
        else:
            table.add_row(str(build_number), style="cyan")
    console.print(table)

    choices = [str(i) for i in data_list]

    chosen_build = Prompt.ask(
        f"Choose a build of paper {version}",
        choices=choices,
        show_choices=False,
        default=choices[-1],
    )

    return chosen_build


def download_jar(url: str, file_name: str, chunk_size=1024):
    """
    Download jar with progress bar.
    """
    request = requests.get(url, stream=True, timeout=60)
    total = int(request.headers.get("content-length", 0))
    with Progress() as progress:
        download_task = progress.add_task(
            f"[yellow]Downloading {file_name}", total=total
        )

        with open(file_name, "wb") as file:
            for data in request.iter_content(chunk_size=chunk_size):
                size = file.write(data)

                if not progress.finished:
                    progress.update(download_task, advance=size)


if __name__ == "__main__":
    console = Console()

    API_BASE = "https://api.papermc.io/v2/"

    VERSION = get_version(api_base=API_BASE)
    BUILD = get_build(api_base=API_BASE, version=VERSION)
    JAR_FILE = f"paper-{VERSION}-{BUILD}.jar"

    DOWNLOAD_URL = f"{API_BASE}/projects/paper/versions/{VERSION}/builds/{BUILD}/downloads/{JAR_FILE}"

    if Confirm.ask(f"Do you wish to download {JAR_FILE}?", default="y"):
        download_jar(url=DOWNLOAD_URL, file_name=JAR_FILE)
        console.print("[green]Download complete!")
    else:
        console.print("[red]Download canceled!")
