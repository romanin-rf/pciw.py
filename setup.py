import os
import setuptools
import pciw

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

# * Ну, setup
setuptools.setup(
	name=pciw.__name__,
	version=pciw.__version__,
	description='Allows you to retrieve information about the system.',
	keywords=['pciw', 'pciw.py'],
	packages=setuptools.find_packages(),
	author_email='semina054@gmail.com',
	url="https://github.com/romanin-rf/pciw.py",
	long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
	long_description_content_type="text/markdown",
	package_data={
        "pciw": globalizer(
            os.path.join(os.path.dirname(__file__), "pciw", "data")
        )
    },
	include_package_data=True,
	author='ProgrammerFromParlament',
	license='MIT',
	install_requires=["screeninfo", "py-cpuinfo", "python-dateutil", "rich", "enhanced-versioning", "pynvml"],
    setup_requires=["screeninfo", "py-cpuinfo", "python-dateutil", "rich", "enhanced-versioning", "pynvml"]
)