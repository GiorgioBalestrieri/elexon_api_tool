from setuptools import setup, find_packages
from os import path
from io import open

_here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(_here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='elexon_api',
    version='0.2.0',
    description=('Elexon API wrapper.'),
    author='Giorgio Balestrieri',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
    install_requires=['requests', 'pandas', 'xmltodict', 'aiohttp', 'asyncio']
    )