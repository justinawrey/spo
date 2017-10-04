"""Spo - A simple command line controller for Spotify!

Usage:
  spo [play | pause | prev | next | replay | save | delete]
  spo (song | artist | album) <search-terms>...
  spo search <search-terms>... [-n=<n> | --num=<n>]
  spo recent [-n=<n> | --num=<n>]
  spo vol (up | down) <amt>
  spo (shuffle | repeat) (on | off)
  spo (-h | --help)
  spo (-v | --version)

Options:
  no arguments                      show currently playing song
  play                              play current song
  pause                             pause current song
  replay                            replay current song
  prev                              previous song
  next                              next song
  save                              save current song to my music
  delete                            deletes current song from my music
  song <search-terms>               quickplay song
  artist <search-terms>             quickplay artist
  album <search-terms>              quickplay album
  search <search-terms> --num NUM   do keyword search and navigate through best matches [default: 5]
  recent --num NUM                  show and navigate through recently played songs [default: 10]
  shuffle (on | off)                turn shuffle mode on or off
  repeat (on | off)                 turn repeat mode on or off
  vol (up | down) <amt>             tweak spotify client volume up/down by amt (0-100)
  -n NUM --num NUM                  number of search/recently played results to display [default: 5]
  -h --help                         show this help message
  -v --version                      show version

"""

# external packages
from docopt import docopt

# from within this project
from .api import *
from .version import __VERSION__


def main():
    """
    Main function and script entry-point. Script will authenticate when needed, and
    refresh authentication when needed with user explicitly refreshing api tokens.
    """

    # check if authenticated
    tokens = get_tokens()
    if not tokens:
        authenticate()

    # refresh if needed
    else:
        refresh_token = tokens["refresh_token"]
        last_refreshed = tokens["last_refreshed"]
        expires_in = tokens["expires_in"]
        curr_time = time.time()
        if curr_time - last_refreshed > expires_in:
            refresh_tokens(refresh_token)

    # parse command line args
    args = docopt(__doc__, version=__VERSION__)

    # handle any control commands inputted by user
    if args["play"]:
        play()

    elif args["pause"]:
        pause()

    elif args["prev"]:
        prev_song()

    elif args["next"]:
        next_song()

    elif args["replay"]:
        replay()

    elif args["save"]:
        save()

    elif args["delete"]:
        delete()

    elif args["song"]:
        search_terms = args["<search-terms>"]
        quickplay("song", *search_terms)

    elif args["artist"]:
        search_terms = args["<search-terms>"]
        quickplay("artist", *search_terms)

    elif args["album"]:
        search_terms = args["<search-terms>"]
        quickplay("album", *search_terms)

    elif args["search"]:
        search_terms = args["<search-terms>"]
        search_amt = args["--num"]
        if int(search_amt) >= 1 and int(search_amt) <= 50:
            search(search_amt, *search_terms)
        else:
            print("Optional argument --num must be in range [1,50]")

    elif args["recent"]:
        search_amt = args["--num"]
        if int(search_amt) >= 1 and int(search_amt) <= 50:
            recent(search_amt)
        else:
            print("Optional argument --num must be in range [1,50]")

    elif args["vol"]:
        tweak_amt = int(args["<amt>"])
        up_or_down = args["up"]
        volume(up_or_down, tweak_amt)

    elif args["shuffle"]:
        on_or_off = args["on"]
        shuffle(on_or_off)

    elif args["repeat"]:
        on_or_off = args["on"]
        repeat(on_or_off)

    else:
        curr_song()


if __name__ == "__main__":
    main()
