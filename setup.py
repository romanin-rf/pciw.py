import os
import setuptools
import pciw

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
	author='ProgrammerFromParlament',
	license='MIT',
	install_requires=["screeninfo", "py-cpuinfo", "python-dateutil", "rich"],
    setup_requires=["screeninfo", "py-cpuinfo", "python-dateutil", "rich"]
)