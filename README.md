# SpotiCLI

SpotiCLI is a simple command line interface for Spotify.  Keep control of your music from the comfort of your terminal!

### A quick rundown:
*  song control: _play, pause, prev,_ and _next_ song
*  search and quickplay best matching _song, artist,_ or _album_ (I'm feeling lucky!)
*  search and choose best matching _song, artist,_ or _album_ from results list

For Spotify free users, ads will stay play when navigating through songs.  **_Oh boy!_**

**Currently Python 3 and Linux/Unix only.**

### Installation

Via everyones favorite package manager:

```python
pip install spoticli
```
or a classic:
```python
python setup.py install
```
**Make sure your pip / python commands above invoke their Python 3 equivalents.**

### Requirements:

The installation methods above should automatically install all requirements.  

These are:
1. [docopt](https://github.com/docopt/docopt)
2. [spotipy](https://github.com/plamere/spotipy)
3. [dbus-python](https://pypi.python.org/pypi/dbus-python/)
4. [requests](https://github.com/kennethreitz/requests)

### Getting Started:

Play a _song, artist,_ or _album_ via quickplay:

```
justin:~$ spoticli song never gonna give you up
Song:	Never Gonna Give You Up
Artist:	Rick Astley
Album:	Whenever You Need Somebody
```

Basic song navigation:

```
justin:~$ spoticli album dark side of the moon
Song:	Speak to Me
Artist:	Pink Floyd
Album:	The Dark Side of the Moon
```

```
justin:~$ spoticli next
Song:	Breathe (In the Air)
Artist:	Pink Floyd
Album:	The Dark Side of the Moon
```

```
justin:~$ spoticli prev
Song:	Speak to Me
Artist:	Pink Floyd
Album:	The Dark Side of the Moon
```

Choose a song, artist, or album via results list:

```
justin:~$ spoticli list song sandstorm

Song                        Artist                  Album                                                                
=========================================================================================================================
Sandstorm - Radio Edit      Darude                  Sandstorm                                                            
Sandstorm - Original Mix    Darude                  Sandstorm                                                            
Sandstorm - Radio Edit      Darude                  Before The Storm                                                     
Sandstorm                   Moon Hooch              Joshua Tree - EP                                                     
Sandstorm Woman             Sleepy Sun              Fever                                                                
Sandstorm - JS 16 Remix     Darude                  Sandstorm                                                            
Sandstorm - Ariel Remix     Darude                  Sandstorm                                                            
Sandstorm                   David Garrett           Music                                                                
Sandstorm                   DJ Crazy J Rodriguez    Dubstep, Vol. 8                                                      
Sandstorm                   Michael McCann          Deus Ex: Mankind Divided (Original Soundtrack - Extended Edition)    


move down:	<j>
move up:	<k>
play selection:	<enter>
quit:		<q> or <esc>
```

### Full functionality:

```
justin:~$ spoticli --help
SpotiCLI - A simple command line controller for Spotify!

Usage:
  spoticli [play | pause | prev | next]
  spoticli (song | artist | album) <search-terms>...
  spoticli list (song | artist | album) <search-terms>... [-n=<n> | --num=<n>]
  spoticli (-h | --help)
  spoticli (-v | --version)

Options:
  no arguments                      show currently playing song
  play                              play/pause current song
  pause                             pause current song
  prev                              previous song
  next                              next song
  song <search-terms>               play best matching song
  artist <search-terms>             play best matching artist
  album <search-terms>              play best matching album
  list song <search-terms>          list num best matching songs
  list artist <search-terms>        list num best matching artists
  list album <search-terms>         list num best matching albums
  -n NUM --num NUM                  number of results to display [default: 10]
  -h --help                         show this help message
  -v --version                      show version
```
