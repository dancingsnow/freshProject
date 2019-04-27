# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sgcc_server import VERSION

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

install_packages = []
# with open('requirements.txt') as f:
#     while True:
#         line = f.readline()
# 	if not line:
# 	    break
#     	line = line.strip('\n')
#     	install_packages.append(line)



setup(
    name='sgcc-server',
    version=VERSION,

    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data = {
            'sgcc_server':['*.html']
        },
    install_requires=install_packages,
    entry_points={
        'console_scripts': [
            'sgcc-server-start=sgcc_server.entry:main',
        ]
    }
)