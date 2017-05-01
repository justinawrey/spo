# spo

spo is a simple command line interface for Spotify.  Keep control of your music from the comfort of your terminal!

## A quick rundown:
*  song control: _play, pause, prev,_ and _next_ song
*  search and quickplay best matching _song, artist,_ or _album_ (I'm feeling lucky!)
*  search and choose best matching _song, artist,_ or _album_ from results list

For Spotify free users, ads will stay play when navigating through songs.  **_Oh boy!_**

**Currently Python 3 and Linux/Unix only.**

```
justin:~$ spo --help
spo - A simple command line controller for Spotify!

Usage:
  spo [play | pause | prev | next]
  spo (song | artist | album) <search-terms>...
  spo list (song | artist | album) <search-terms>... [-n=<n> | --num=<n>]
  spo (-h | --help)
  spo (-v | --version)

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

## Installation

Via everyones favorite package manager:

```python
pip install spo
```
or a classic:
```python
python setup.py install
```
**Make sure your pip / python commands above invoke their Python 3 equivalents.**

## Requirements:

The installation methods above should automatically install all requirements.  

These are:
1. [docopt](https://github.com/docopt/docopt)
2. [spotipy](https://github.com/plamere/spotipy)
3. [dbus-python](https://pypi.python.org/pypi/dbus-python/)
4. [requests](https://github.com/kennethreitz/requests)

## Getting Started:

Play a _song, artist,_ or _album_ via quickplay:

```
justin:~$ spo song never gonna give you up
Song:	Never Gonna Give You Up
Artist:	Rick Astley
Album:	Whenever You Need Somebody
```

```
justin:~$ spo album dark side of the moon
Song:	Speak to Me
Artist:	Pink Floyd
Album:	The Dark Side of the Moon
```

Basic song navigation:

```
justin:~$ spo next
Song:	Breathe (In the Air)
Artist:	Pink Floyd
Album:	The Dark Side of the Moon
```

```
justin:~$ spo prev
Song:	Speak to Me
Artist:	Pink Floyd
Album:	The Dark Side of the Moon
```

Search and select a song, artist, or album via results list:

```
justin:~$ spo list song sandstorm

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

```
justin:~$ spo list artist tiny tim

Artist                                  
========================================
Tiny Tim                                
Tiny Tim w/ The New Duncan Imperials    
Tiny Legs Tim                           
DJ Tiny Tim                             
Tiny Tim with Gary Owens                
Tiny Tim with Harry Roy & His Band      
Tiny Tim's Family                       


move down:	<j>
move up:	<k>
play selection:	<enter>
quit:		<q> or <esc>
```

Search and select songs from a particular artist or album:

```
justin:~$ spo list song blink 182

Song                     Artist       Album                             
========================================================================
I Miss You               blink-182    blink-182                         
All The Small Things     blink-182    Enema Of The State                
What's My Age Again?     blink-182    Enema Of The State                
She's Out Of Her Mind    blink-182    California                        
Feeling This             blink-182    blink-182                         
Bored To Death           blink-182    California                        
Adam's Song              blink-182    Enema Of The State                
Parking Lot              blink-182    Parking Lot                       
First Date               blink-182    Take Off Your Pants And Jacket    
Down                     blink-182    blink-182                         


move down:	<j>
move up:	<k>
play selection:	<enter>
quit:		<q> or <esc>
```
