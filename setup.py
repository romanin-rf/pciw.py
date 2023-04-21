import os
import json
import pciw
import setuptools
from wheel.bdist_wheel import bdist_wheel

try: 
    with open("build.json") as file: data = json.load(file)
except:
    data = {
        "cmdclass": ["py3", "none", "any"],
        "package_data_paths": [
            os.path.join(os.path.dirname(__file__), "pciw", "data")
        ]
    }

# * Функция получения полных путей к файлам в папках и подпапках
def globalizer(dirpath: str) -> list:
    files = []
    folder_abspath = os.path.abspath(dirpath)
    if os.path.isdir(folder_abspath):
        for i in os.listdir(folder_abspath):
            path = folder_abspath + os.sep + i
            if os.path.isdir(path):
                for _i in globalizer(path):
                    files.append(_i)
            elif os.path.isfile(path):
                files.append(path)
    elif os.path.isfile(folder_abspath):
        files.append(folder_abspath)
    return files

def generate_cmdclass(version: str="py3", abi: str="none", system_tag: str="any"):
    class bdist_wheel_tag_name(bdist_wheel):
        def get_tag(self): return version, abi, system_tag
    return {'bdist_wheel': bdist_wheel_tag_name}

def generate_pdp() -> list:
    pdp = []
    for i in data["package_data_paths"]:
        pdp += globalizer(i)
    return pdp

DEFAULT_ARGS = dict(
	name=pciw.__name__,
	version=pciw.__version__,
	description='Allows you to retrieve information about the system.',
	keywords=['pciw', 'pciw.py'],
	packages=setuptools.find_packages(),
	author_email='semina054@gmail.com',
	url="https://github.com/romanin-rf/pciw.py",
	long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
	long_description_content_type="text/markdown",
	include_package_data=True,
	author='ProgrammerFromParlament',
	license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
	install_requires=["screeninfo", "py-cpuinfo", "python-dateutil", "rich", "pynvml", "elevate"],
    setup_requires=["screeninfo", "py-cpuinfo", "python-dateutil", "rich", "pynvml", "elevate"]
)

setuptools.setup(
    **DEFAULT_ARGS,
    cmdclass=generate_cmdclass(*data["cmdclass"]),
    package_data={"pciw": generate_pdp()}
)