"""Spo - A simple command line controller for Spotify!

Usage:
  spo [play | pause | prev | next | replay | save]
  spo (song | artist | album) <search-terms>...
  spo search <search-terms>... [-n=<n> | --num=<n>]
  spo recent [-n=<n> | --num=<n>]
  spo vol (up | down) [-t=<t> | --tweak=<t>]
  spo (shuffle | repeat) (on | off)
  spo (-h | --help)
  spo (-v | --version)

Options:
  no arguments                     show currently playing song
  play                             play current song
  pause                            pause current song
  replay                           replay current song
  prev                             previous song
  next                             next song
  save                             save current song to my music
  song <search-terms>              quickplay song
  artist <search-terms>            quickplay artist
  album <search-terms>             quickplay album
  search <search-terms>            do keyword search and navigate through best matches
  recent                           show and navigate through recently played songs
  shuffle (on | off)               turn shuffle mode on or off
  repeat (on | off)                turn repeat mode on or off
  vol (up | down)                  tweak spotify client volume up/down by 5%
  -n NUM --num NUM                 number of search/recently played results to display [default: 10]
  -t NUM --tweak NUM               percentage by which volume should be tweaked [default: 5]
  -h --help                        show this help message
  -v --version                     show version

"""
# std packages
import time
import os

# external packages
from docopt import docopt

# from within this project
from spo.version import __VERSION__
from spo.listutil import PrettyListCreator
from spo.getch import Getch
from spo.apicaller import APICaller

#returns the uri of selection on enter key press
def let_user_scroll(results_array, results_len):
    results_array_length = len(results_array)
    list_creator = PrettyListCreator(list(results_array.values()))
    list_creator.reprint(list_creator.pretty_list(0))
    getch = Getch()
    index = 0
    while(True):
        user_input = getch()
        if user_input == 'q' or user_input == '\x1B':
            return None
        elif user_input == 'j' and index < results_array_length - 1:
            index += 1
            list_creator.reprint(list_creator.pretty_list(index))
        elif user_input == 'k' and index > 0:
            index -= 1
            list_creator.reprint(list_creator.pretty_list(index))
        elif user_input == '\x0D':
            list_creator.reprint('')
            list_creator.moveup(results_len + 10)
            return list(results_array.keys())[index]

def main():
    args = docopt(__doc__, version=__VERSION__)

    # try to set up dbus and relevant ctl/property interfaces
    # if we get an error, spotify is not open... prompt y/n to open
    try:
        player = dbus.SessionBus().get_object(DBUS_SPOTIFY, DBUS_OBJECT_PATH)
        ctl_interface = dbus.Interface(player, dbus_interface=DBUS_CTL_INTERFACE)
        property_interface = dbus.Interface(player, dbus_interface=DBUS_PROP_INTERFACE)
        api_caller = APICaller()
    except dbus.DBusException:
        getch = Getch()
        print('Error: cannot connect to spotify')
        print('Would you like to launch spotify client? (y/n)')
        if getch() == 'y':
            print('launching spotify...')
            os.system('spotify --minimized & > /dev/null')
            print('spotify launched successfully')
            # allow spotify to start up and send play -> pause commands in order to 'register' 
            # the current song with spotify desktop player.  
            # This is necessary for following dbus commands to work
            time.sleep(2)
            player = dbus.SessionBus().get_object(DBUS_SPOTIFY, DBUS_OBJECT_PATH)
            ctl_interface = dbus.Interface(player, dbus_interface=DBUS_CTL_INTERFACE)
            ctl_interface.Play()
            ctl_interface.Pause()
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

    # spotify MPRIS support is very limited and does not support isolated volume control
    # this volume tweak uses amixer to tweak overall system volume
    elif args['vol']: # tweak volume by 5%
        if args['up']:
            os.system(VOL_UP)
        else:
            os.system(VOL_DOWN)
        return

    elif args['search']: # list search results
        results_array = api_caller.get_search_result_dict(args['<search-terms>'], 'tracks', args['--num'])
        if results_array:
            user_selection = let_user_scroll(results_array, len(results_array))
            if user_selection:
                ctl_interface.OpenUri(user_selection)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return

    elif args['song']: # play song
        track_uri = api_caller.search_and_get_uri(args['<search-terms>'], 'tracks')
        if track_uri:
            ctl_interface.OpenUri(track_uri)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return

    elif args['artist']: # play artist
        artist_uri = api_caller.search_and_get_uri(args['<search-terms>'], 'artists')
        if artist_uri:
            ctl_interface.OpenUri(artist_uri)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return

    elif args['album']: # play album
        album_uri = api_caller.search_and_get_uri(args['<search-terms>'], 'albums')
        if album_uri:
            ctl_interface.OpenUri(album_uri)
        else:
            print("No results found for query: " + ' '.join(args['<search-terms>']))
            return
    
    # show the currently selected song
    # allow a short delay to account for delay in dbus song retrieval, so we show the correct song
    time.sleep(0.25)
    track_metadata = property_interface.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    print("Song:\t" + track_metadata['xesam:title'] if 'xesam:title' in track_metadata else 'Unknown')
    print("Artist:\t" + track_metadata['xesam:artist'][0] if 'xesam:artist' in track_metadata else 'Unknown')
    print("Album:\t" + track_metadata['xesam:album'] if 'xesam:album' in track_metadata else 'Unknown')

if __name__ == "__main__":
    main()
