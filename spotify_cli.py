import argparse
import spotipy
import os

parser = argparse.ArgumentParser(description="simple spotify from the command line")

# Add arguments here
# mutually exclusive prev, tog, next
prev_tog_next = parser.add_mutually_exclusive_group()
prev_tog_next.add_argument('-p', "--prev", action="store_true", help="previous song")
prev_tog_next.add_argument('-t', "--toggle", action="store_true", help="toggle current song")
prev_tog_next.add_argument('-n', "--next", action="store_true", help="next song")

# toggle queue
# toggle verbose

# End add arguments here

args = parser.parse_args()

# Start code here
if args.prev:
    os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous >/dev/null")
elif args.toggle:
    os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause >/dev/null")
elif args.next:
    os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next >/dev/null")
