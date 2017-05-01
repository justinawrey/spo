spo
========

spo is a simple command line interface for Spotify. Keep control of
your music from the comfort of your terminal!

A quick rundown:
----------------

-  song control: *play, pause, prev,* and *next* song
-  search and quickplay best matching *song, artist,* or *album* (I'm
   feeling lucky!)
-  search and choose best matching *song, artist,* or *album* from
   results list

For Spotify free users, ads will stay play when navigating through
songs. ***Oh boy!***

**Currently Python 3 and Linux/Unix only.**

::

    justin:~$ spo --help
    Spo - A simple command line controller for Spotify!

    Usage:
      spo [play | pause | prev | next | save]
      spo (song | artist | album) <search-terms>...
      spo search <search-terms>... [-n=<n> | --num=<n>]
      spo vol (up | down)
      spo (-h | --help)
      spo (-v | --version)

    Options:
      no arguments                      show currently playing song
      play                              play/pause current song
      pause                             pause current song
      prev                              previous song
      next                              next song
      save                              save song to my music (requires auth)
      song <search-terms>               quickplay song
      artist <search-terms>             quickplay artist
      album <search-terms>              quickplay album
      search <search-terms>             do keyword search and list best matches
      vol (up | down)                   tweak volume up/down by 5%
      -n NUM --num NUM                  number of search results to display [default: 10]
      -h --help                         show this help message
      -v --version                      show version

Installation
------------

Via everyones favorite package manager:

.. code:: python

    pip install spo

or a classic:

.. code:: python

    python setup.py install

**Make sure your pip / python commands above invoke their Python 3
equivalents.**

Requirements:
-------------

The installation methods above should automatically install all
requirements.

These are: 1. `docopt <https://github.com/docopt/docopt>`__ 2.
`spotipy <https://github.com/plamere/spotipy>`__ 3.
`dbus-python <https://pypi.python.org/pypi/dbus-python/>`__ 4.
`requests <https://github.com/kennethreitz/requests>`__

Getting Started:
----------------

Play a *song, artist,* or *album* via quickplay:

::

    justin:~$ spo song never gonna give you up
    Song:   Never Gonna Give You Up
    Artist: Rick Astley
    Album:  Whenever You Need Somebody

::

    justin:~$ spo album dark side of the moon
    Song:   Speak to Me
    Artist: Pink Floyd
    Album:  The Dark Side of the Moon

Basic song navigation:

::

    justin:~$ spo next
    Song:   Breathe (In the Air)
    Artist: Pink Floyd
    Album:  The Dark Side of the Moon

::

    justin:~$ spo prev
    Song:   Speak to Me
    Artist: Pink Floyd
    Album:  The Dark Side of the Moon

Search and select a song, artist, or album via results list:

::

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


    move down:  <j>
    move up:    <k>
    play selection: <enter>
    quit:       <q> or <esc>

::

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


    move down:  <j>
    move up:    <k>
    play selection: <enter>
    quit:       <q> or <esc>

Search and select songs from a particular artist or album:

::

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


    move down:  <j>
    move up:    <k>
    play selection: <enter>
    quit:       <q> or <esc>
