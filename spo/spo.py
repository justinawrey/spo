"""Spo - A simple command line controller for Spotify!

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

"""
import dbus
import spotipy
import time
import os
from docopt import docopt
from collections import OrderedDict
from version import __version__
from listcreator import PrettyListCreator
from getch import Getch

DBUS_BUS_NAME_SPOTIFY = "org.mpris.MediaPlayer2.spotify"
DBUS_OBJECT_PATH = "/org/mpris/MediaPlayer2"
VOL_UP = "amixer -q -D pulse sset Master 5%+"
VOL_DOWN = "amixer -q -D pulse sset Master 5%-"

def search_and_get_uri(searched_keywords, search_type):
    search_data = spotipy.Spotify().search(' '.join(searched_keywords), limit=1, type=search_type[:-1])
    # get track URI of first result and play it with dbus
    if search_data[search_type]['items']:
        return search_data[search_type]['items'][0]['uri']
    else:
        return None

def get_search_result_dict(searched_keywords, search_type, num_results=10):
    rtn_dict = OrderedDict()
    search_data = spotipy.Spotify().search(' '.join(searched_keywords), limit=num_results, type=search_type[:-1])
    if search_data[search_type]['items']:
        for item in search_data[search_type]['items']:
            if search_type == 'tracks':
                rtn_dict[item['uri']] = [item['name'], item['artists'][0]['name'], item['album']['name']]
            elif search_type == 'artists':
                rtn_dict[item['uri']] = [item['name']]
            elif search_type == 'albums':
                rtn_dict[item['uri']] = [item['name'], item['artists'][0]['name']]
        return rtn_dict
    else:
        return None

def let_user_scroll(results_array, results_len): #returns the uri of selection on enter key press
    results_array_length = len(results_array)
    listCreator = PrettyListCreator(list(results_array.values()))
    listCreator.reprint(listCreator.pretty_list(0))
    getch = Getch()
    index = 0
    while(True):
        user_input = getch()
        if user_input == 'q' or user_input == '\x1B':
            return None
        elif user_input == 'j' and index < results_array_length - 1:
            index += 1
            listCreator.reprint(listCreator.pretty_list(index))
        elif user_input == 'k' and index > 0:
            index -= 1
            listCreator.reprint(listCreator.pretty_list(index))
        elif user_input == '\x0D':
            listCreator.reprint('')
            listCreator.moveup(results_len + 10)
            return list(results_array.keys())[index]

def main():
    args = docopt(__doc__, version=__version__)

    # try to set up dbus and relevant ctl/property interfaces
    # if we get an error, spotify is not open... do this here so optional args still work
    try:
        player = dbus.SessionBus().get_object(DBUS_BUS_NAME_SPOTIFY, DBUS_OBJECT_PATH)
        ctl_interface = dbus.Interface(player, dbus_interface="org.mpris.MediaPlayer2.Player")
        property_interface = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
    except dbus.DBusException:
        getch = Getch()
        print('Error: cannot connect to spotify')
        print('Would you like to launch spotify client? (y/n)')
        if getch() == 'y':
            print('launching spotify...')
            os.system('spotify --minimized & > /dev/null')
            print('spotify launched successfully')
        else:
            print('aborting...')
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

    elif args['save']: # save song to my music (requires user authentication)
        return

    elif args['vol']: # tweak volume by 5%
        if args['up']:
            os.system(VOL_UP)
        else:
            os.system(VOL_DOWN)
        return

    elif args['search']: # list search results
        results_array = get_search_result_dict(args['<search-terms>'], 'tracks', args['--num'])
        if results_array:
            user_selection = let_user_scroll(results_array, len(results_array))
            if user_selection:
                ctl_interface.OpenUri(user_selection)
            else:
                return
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return

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
    time.sleep(0.5)

    # get currently playing song and display its data
    track_metadata = property_interface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    print("Song:\t" + track_metadata['xesam:title'] if 'xesam:title' in track_metadata else 'Unknown')
    print("Artist:\t" + track_metadata['xesam:artist'][0] if 'xesam:artist' in track_metadata else 'Unknown')
    print("Album:\t" + track_metadata['xesam:album'] if 'xesam:album' in track_metadata else 'Unknown')

if __name__ == "__main__":
    main()
