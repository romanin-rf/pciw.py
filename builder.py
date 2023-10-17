import os
import sys
import subprocess
import click
import json
from rich.console import Console

# ! Other
LOCALDIR = os.path.dirname(__file__)
console = Console()

# ! Main
@click.command()
@click.option(
    "--python_version", "-pv",
    type=str,
    default="py3",
    show_default=True
)
@click.option(
    "--abi",
    type=str,
    default="none",
    show_default=True
)
@click.option(
    "--sys_tag", "-st",
    type=str,
    default="any",
    show_default=True
)
@click.option(
    "--package_data_paths", "-pdp",
    type=str,
    default="{localdir}{sep}pciw{sep}data",
    show_default=True
)
def Main(python_version: str, abi: str, sys_tag: str, package_data_paths: str):
    build_config = {
        "cmdclass": [python_version, abi, sys_tag],
        "package_data_paths": [str(i).format(localdir=LOCALDIR, sep=os.sep) for i in package_data_paths.split(",")]
    }
    console.print(build_config)
    with open("build.json", "w") as file: json.dump(build_config, file)
    try: subprocess.check_output([sys.executable, os.path.join(LOCALDIR, "setup.py"), "bdist_wheel"])
    except: console.print_exception()

if __name__ == '__main__':
    Main()