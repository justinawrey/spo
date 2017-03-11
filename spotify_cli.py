import argparse
import spotipy
import os
import pickle
import dbus

pickle_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mypickle.pk")

DBUS_BUS_NAME_SPOTIFY = "org.mpris.MediaPlayer2.spotify"
DBUS_OBJECT_PATH = "/org/mpris/MediaPlayer2"

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="simple spotify from the command line\ndefault behaviour (no arguments): show current song")

    # Add arguments here
    # mutually exclusive prev, tog, next
    prev_tog_next = parser.add_mutually_exclusive_group()
    prev_tog_next.add_argument('-p', "--prev", action="store_true", help="previous song")
    prev_tog_next.add_argument('-t', "--toggle", action="store_true", help="toggle current song")
    prev_tog_next.add_argument('-n', "--next", action="store_true", help="next song")

    parser.add_argument('-q', "--show-queue", choices=["on", "off"], help="toggles viewing song queue")
    parser.add_argument('-v', "--verbose", choices=["on", "off"], help="toggles verbose song information")
    # End add arguments here

    args = parser.parse_args()

    # Start code here

    # retrieve pickled toggle options data
    # if this is the first run through, skip this, as .pk file doesn't exist
    toggle_options = {'show_queue': 'off', 'verbose': 'off'}
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as _file:
            toggle_options = pickle.load(_file)

    # check if queue or verbose mode has been turned on
    if args.show_queue:
        toggle_options['show_queue'] = args.show_queue
    if args.verbose:
        toggle_options['verbose'] = args.verbose

    # pickle the config data to a .pk file in local dir
    with open(pickle_file, 'wb+') as _file:
        pickle.dump(toggle_options, _file)

    # set up dbus and
    # send any control commands inputted by user
    player = dbus.SessionBus().get_object(DBUS_BUS_NAME_SPOTIFY, DBUS_OBJECT_PATH)
    ctl_interface = dbus.Interface(player, dbus_interface="org.mpris.MediaPlayer2.Player")

    if args.prev:
        ctl_interface.Previous()
    elif args.toggle:
        ctl_interface.PlayPause()
    elif args.next:
        ctl_interface.Next()

if __name__ == "__main__":
    main()
