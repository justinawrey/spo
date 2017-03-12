import argparse
import os
import dbus
import time
import spotipy
import sys

pickle_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mypickle.pk")

DBUS_BUS_NAME_SPOTIFY = "org.mpris.MediaPlayer2.spotify"
DBUS_OBJECT_PATH = "/org/mpris/MediaPlayer2"

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="simple spotify from the command line\ndefault behaviour (no arguments): show current song")

    # Add arguments here
    # mutually exclusive prev, tog, next
    prev_tog_next_search = parser.add_mutually_exclusive_group()
    prev_tog_next_search.add_argument('-p', "--prev", action="store_true", help="previous song")
    prev_tog_next_search.add_argument('-t', "--toggle", action="store_true", help="toggle current song")
    prev_tog_next_search.add_argument('-n', "--next", action="store_true", help="next song")
    prev_tog_next_search.add_argument('-s', "--search", type=str, nargs='+', help="search keywords and play the first match")
    # End add arguments here

    args = parser.parse_args()

    # set up dbus and relevant ctl/property interfaces
    player = dbus.SessionBus().get_object(DBUS_BUS_NAME_SPOTIFY, DBUS_OBJECT_PATH)
    ctl_interface = dbus.Interface(player, dbus_interface="org.mpris.MediaPlayer2.Player")
    property_interface = dbus.Interface(player, dbus_interface='org.freedesktop.DBus.Properties')

    # send any control commands inputted by user
    if args.prev:
        ctl_interface.Previous()
    elif args.toggle:
        ctl_interface.PlayPause()
        sys.exit()
    elif args.next:
        ctl_interface.Next()
    elif args.search:
        search_data = spotipy.Spotify().search(' '.join(args.search), limit=1)

        # get URI of first result and play it with dbus
        if search_data['tracks']['items']:
            ctl_interface.OpenUri(search_data['tracks']['items'][0]['uri'])
        else:
            print("No results found for query: " + ' '.join(args.search))
            sys.exit()

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
