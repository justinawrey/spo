"""SpotiCLI - A simple command line controller for Spotify!

Usage:
  spoticli [play | pause | prev | next]
  spoticli (song | artist | album) <search-terms>...
  spoticli list (song | artist | album) <search-terms>...
  spoticli (-h | --help)
  spoticli (-v | --version)

Options:
  no arguments                     show currently playing song
  play                             play/pause current song
  pause                            pause current song
  prev                             previous song
  next                             next song
  song <search-terms>              play best matching song
  artist <search-terms>            play best matching artist
  album <search-terms>             play best matching album
  list song <search-terms>         list best matching songs
  list artist <search-terms>       list best matching artists
  list album <search-terms>        list best matching albums
  -h --help                        show this help message
  -v --version                     show version

"""
from docopt import docopt
import dbus
import spotipy
import time
from version import __version__

DBUS_BUS_NAME_SPOTIFY = "org.mpris.MediaPlayer2.spotify"
DBUS_OBJECT_PATH = "/org/mpris/MediaPlayer2"

def search_and_get_uri(searched_keywords, search_type):
    search_data = spotipy.Spotify().search(' '.join(searched_keywords), limit=1, type=search_type[:-1])
    # get track URI of first result and play it with dbus
    if search_data[search_type]['items']:
        return search_data[search_type]['items'][0]['uri']
    else:
        return None

def main():

    args = docopt(__doc__, version=__version__)

    # try to set up dbus and relevant ctl/property interfaces
    # if we get an error, spotify is not open... do this here so optional args still work
    try:
        player = dbus.SessionBus().get_object(DBUS_BUS_NAME_SPOTIFY, DBUS_OBJECT_PATH)
        ctl_interface = dbus.Interface(player, dbus_interface="org.mpris.MediaPlayer2.Player")
        property_interface = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
    except dbus.DBusException:
        print('Error: cannot connect to spotify')
        print('Please start spotify client')
        return

    # send any control commands inputted by user
    if args['prev']: # prev song
        ctl_interface.Previous()
    elif args['play']: # play/pause song
        ctl_interface.PlayPause()
        return
    elif args['pause']: # pause song
        ctl_interface.Pause()
        return
    elif args['next']: # next song
        ctl_interface.Next()
    elif args['list'] and args['song']: # list song
        pass
    elif args['list'] and args['artist']: # list artist
        pass
    elif args['list'] and args['album']: # list album
        pass
    elif args['song']: # play song
        track_uri = search_and_get_uri(args['<search-terms>'], 'tracks')
        if track_uri:
            ctl_interface.OpenUri(track_uri)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return
    elif args['artist']: # play artist
        artist_uri = search_and_get_uri(args['<search-terms>'], 'artists')
        if artist_uri:
            ctl_interface.OpenUri(artist_uri)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return
    elif args['album']: # play album
        album_uri = search_and_get_uri(args['<search-terms>'], 'albums')
        if album_uri:
            ctl_interface.OpenUri(album_uri)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return

    # add a small delay so dbus retrieves the correct information in the event
    # that the song was just switched
    time.sleep(0.1)

    # get currently playing song and display its data
    track_metadata = property_interface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    print("Song:\t" + track_metadata['xesam:title'] if 'xesam:title' in track_metadata else 'Unknown')
    print("Artist:\t" + track_metadata['xesam:artist'][0] if 'xesam:artist' in track_metadata else 'Unknown')
    print("Album:\t" + track_metadata['xesam:album'] if 'xesam:album' in track_metadata else 'Unknown')

if __name__ == "__main__":
    main()
