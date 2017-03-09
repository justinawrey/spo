import argparse
import spotipy
import os
import pickle

pickle_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mypickle.pk")

# control commands to send for linux
SEND_CMD_LINUX_PREV_SONG = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous >/dev/null"
SEND_CMD_LINUX_TOGGLE_SONG = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous >/dev/null"
SEND_CMD_LINUX_NEXT_SONG = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous >/dev/null"

def main():

    parser = argparse.ArgumentParser(description="simple spotify from the command line")

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

    # send any control commands inputted by user
    if args.prev:
        os.system(SEND_CMD_LINUX_PREV_SONG)
    elif args.toggle:
        os.system(SEND_CMD_LINUX_TOGGLE_SONG)
    elif args.next:
        os.system(SEND_CMD_LINUX_NEXT_SONG)

if __name__ == "__main__":
    main()
