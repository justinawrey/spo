from setuptools import setup

exec(open('spoticli/version.py').read())
setup(
    name='SpotiCLI',
    version=__version__,
    author='justinawrey',
    author_email='awreyjustin@gmail.com',
    packages=['spoticli'],
    url='http://pypi.python.org/pypi/SpotiCLI/',
    license='LICENSE.txt',
    description='control Spotify from the command line',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'spoticli = spoticli.spotify_cli:main'
        ]
    },
    install_requires=[
        'dbus-python',
        'spotipy',
        'docopt'
    ]
)

# ADD INSTALL REQUIRES
