from setuptools import setup, find_packages

__version__ = '0.0.1'


setup(
    name = 'vertmetric',
    version = __version__,
    packages = find_packages(exclude=('reports')),
    entry_points = {
        'console_scripts': ['vertmetric = vertmetric.__main__:main']
})
