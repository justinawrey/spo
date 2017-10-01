from setuptools import setup
from spo.version import __VERSION__

setup(
    name='spo',
    version=__VERSION__,
    author='justinawrey',
    author_email='awreyjustin@gmail.com',
    packages=['spo'],
    url='https://github.com/justinawrey/spo',
    license='LICENSE.txt',
    description='control Spotify from the command line',
    long_description=open('README.rst').read(),
    keywords = ['spotify command line interface'],
    entry_points={
        'console_scripts': [
            'spo = spo.__main__:main'
        ]
    },
    install_requires=[
        'docopt'
    ]
)
