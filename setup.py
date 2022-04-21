import os
import setuptools

setuptools.setup(
	name='pciw.py',
	version='0.1',
	description='Allows you to retrieve information about the system.',
	keywords=['pciw', 'pciw.py'],
	packages=setuptools.find_packages(),
	author_email='semina054@gmail.com',
	url="https://github.com/romanin-rf/pciw.py",
	zip_safe=False,
	long_description=open(
		os.path.join(
			os.path.dirname(__file__),
			'README.rst'
		)
	).read(),
	author='ProgrammerFromParlament',
	license='MIT'
)