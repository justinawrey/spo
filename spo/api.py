# std packages
import pickle
import os
import webbrowser
import time
import sys
import json

# external packages
import requests

# internal packages
from .table import print_table

# relevant app information
CLIENT_ID = os.environ["SPO_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPO_CLIENT_SECRET"]
REDIRECT_URI = "http://justinawrey.github.io/spo"
SCOPES = "user-library-modify user-read-playback-state user-read-currently-playing user-modify-playback-state user-read-recently-played"


def get_tokens():
    """
    Returns dict containing current access and refresh tokens, as well as expiry times.
    Returns None if user has not yet authenticated.
    """
    with open("token.pk", "rb") as pickle_file:
        token_data = pickle.load(pickle_file)
    return token_data


def refresh_tokens():
    """
    Refreshes users access and refresh tokens.
    """
    with open("token.pk", "rb") as pickle_file:
        data = pickle.load(pickle_file)

    try:
        resp = requests.post("https://accounts.spotify.com/api/token",
                             data={"grant_type": "refresh_token",
                                   "refresh_token": data["refresh_token"]},
                             auth=(CLIENT_ID, CLIENT_SECRET))
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # pickle refreshed information
    resp_json = resp.json()
    data["access_token"] = resp_json["access_token"]
    data["expires_in"] = resp_json["expires_in"]
    data["received_time"] = time.time()

    with open("token.pk", "wb") as pickle_file:
        pickle.dump(data, pickle_file)


def authenticate():
    """
    Spo follows Spotify Authorization Code Flow
    https://developer.spotify.com/web-api/authorization-guide/

    This function performs the authorization code flow,
    and saves access and refresh tokens.
    """

    # application requests authorization
    # this GET request must be done through browser as the web API returns js to be ran
    auth_req = "https://accounts.spotify.com/authorize" + \
        "?redirect_uri=" + REDIRECT_URI + \
        "&scope=" + SCOPES + \
        "&client_id=" + CLIENT_ID + \
        "&response_type=code"
    auth_req.replace(":", "%3A").replace("/", "%2F").replace(" ", "+")
    webbrowser.open(auth_req)

    # application receives authorization code
    url = input("enter URL:\n")
    if url.find("code="):
        auth_code = url[url.find("code=") + 5:]
    else:
        print("authorization failed... aborting")
        return

    # application requests access tokens and refresh tokens
    try:
        resp = requests.post("https://accounts.spotify.com/api/token",
                             data={"grant_type": "authorization_code",
                                   "redirect_uri": REDIRECT_URI,
                                   "code": auth_code},
                             auth=(CLIENT_ID, CLIENT_SECRET))
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # pickle tokens so user does not have to re-authenticate
    resp_json = resp.json()
    pickle_data = {
        "access_token": resp_json["access_token"],
        "refresh_token": resp_json["refresh_token"],
        "expires_in": resp_json["expires_in"],
        "received_time": time.time(),
    }
    with open("token.pk", "wb") as pickle_file:
        pickle.dump(pickle_data, pickle_file)


def curr_song():
    """
    Shows currently playing song.
    """
    access_token = get_tokens()["access_token"]

    try:
        resp = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    resp_json = resp.json()
    song = resp_json["item"]["name"]
    artist = resp_json["item"]["artists"][0]["name"]
    album = resp_json["item"]["album"]["name"]

    print_table([[song, artist, album]])


def play():
    """
    Plays current song.
    """
    access_token = get_tokens()["access_token"]

    try:
        requests.put("https://api.spotify.com/v1/me/player/play",
                     headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def replay():
    """
    Replays current song.
    """
    access_token = get_tokens()["access_token"]

    try:
        requests.put("https://api.spotify.com/v1/me/player/seek",
                     params={"position_ms": "1"},
                     headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # show what is now playing
    curr_song()


def pause():
    """
    Pauses current song.
    """
    access_token = get_tokens()["access_token"]

    try:
        requests.put("https://api.spotify.com/v1/me/player/pause",
                     headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def shuffle(on_off):
    """
    Turn shuffle mode on or off.
        :param on_off {bool}: whether to set shuffle mode to on or off
    """
    access_token = get_tokens()["access_token"]

    try:
        requests.put("https://api.spotify.com/v1/me/player/shuffle",
                     params={"state": str(on_off).lower()},
                     headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def repeat(on_off):
    """
    Turn repeat mode on or off.
        :param on_off {bool}: whether to set repeat mode to on or off
    """
    access_token = get_tokens()["access_token"]

    if on_off:
        query_val = "track"
    else:
        query_val = "off"

    try:
        requests.put("https://api.spotify.com/v1/me/player/repeat",
                     params={"state": query_val},
                     headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def volume(up_down, amt):
    """
    Set volume to a specific volume.
        :param up_down {bool}: whether to turn the volume up or down
        :param amt {int}: percentage by which to tweak volume (must be nonneg)
    """
    access_token = get_tokens()["access_token"]

    # first get curr volume
    try:
        resp = requests.get("https://api.spotify.com/v1/me/player",
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)
    vol = int(resp.json()["device"]["volume_percent"])

    # compute new volume
    if up_down:
        adjusted_vol = int(vol + int(amt))
        if adjusted_vol > 100:
            adjusted_vol = 100
    else:
        adjusted_vol = int(vol - int(amt))
        if adjusted_vol < 0:
            adjusted_vol = 0

    # tweak volume
    try:
        requests.put("https://api.spotify.com/v1/me/player/volume",
                     params={"volume_percent": str(adjusted_vol)},
                     headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def prev_song():
    """
    Plays the previous song.
    """
    access_token = get_tokens()["access_token"]

    try:
        requests.post("https://api.spotify.com/v1/me/player/previous",
                      headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # display which song is now playing - allow a short delay for player to begin
    # playing prev song before polling song for its metadata
    time.sleep(0.25)
    curr_song()


def next_song():
    """
    Plays the next song.
    """
    access_token = get_tokens()["access_token"]

    try:
        requests.post("https://api.spotify.com/v1/me/player/next",
                      headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # display which song is now playing - allow a short delay for player to begin
    # playing next song before polling song for its metadata
    time.sleep(0.25)
    curr_song()


def save():
    """
    Saves current song to my music.
    """
    access_token = get_tokens()["access_token"]

    # get id of currently playing song
    try:
        resp = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)
    track_id = resp.json()["item"]["id"]

    # save currently playing song to my music
    try:
        requests.put("https://api.spotify.com/v1/me/tracks",
                           params={"ids": track_id},
                           headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def delete():
    """
    Deletes current song from my music.
    """
    access_token = get_tokens()["access_token"]

    # get id of currently playing song
    try:
        resp = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)
    track_id = resp.json()["item"]["id"]

    # delete currently playing song from my music
    try:
        requests.delete("https://api.spotify.com/v1/me/tracks",
                        params={"ids": track_id},
                        headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)


def recent(num):
    """
    Display recently played songs.
        :param num {int}: number of recently played songs to display
    """
    access_token = get_tokens()["access_token"]

    # this endpoint does not supply album names
    try:
        resp = requests.get("https://api.spotify.com/v1/me/player/recently-played",
                            params={"limit": str(num)},
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    to_print = []
    for item in resp.json()["items"]:
        song = item["track"]["name"]
        artist = item["track"]["artists"][0]["name"]
        track_id = item["track"]["id"]  # used to retrieve album name

        # retrieve album name
        try:
            resp = requests.get("https://api.spotify.com/v1/tracks/" + track_id,
                                headers={"Authorization": "Bearer " + access_token})
        except requests.exceptions.RequestException as exception:
            print(exception)
            sys.exit(1)

        album = resp.json()["album"]["name"]
        to_print.append([song, artist, album])

    print_table(to_print)


def search(amt, *args):
    """
    Searches for a song via search terms and lists a table of
    size 'amt' containing search results.
        :param amt=5 {int}: amount of results to show
        :param *args {[string]}: search terms to search with
    """
    access_token = get_tokens()["access_token"]

    try:
        resp = requests.get("https://api.spotify.com/v1/search",
                            params={"q": "+".join(args), "type": "track",
                                    "limit": str(amt)},
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    to_print = []
    for item in resp.json()["tracks"]["items"]:
        song = item["name"]
        artist = item["artists"][0]["name"]
        album = item["album"]["name"]
        to_print.append([song, artist, album])

    print_table(to_print)


def quickplay(option, *args):
    """
    Quickplay a song/artist/album based on search terms.
        :param option {string}:
            song - quickplay track
            artist - quickplay artist
            album - quickplay album
        :param *args {[string]}: search terms to search with
    """
    access_token = get_tokens()["access_token"]

    # we would like to use the key "song" for quickplay song - spotify API uses "track"
    # ...compensate here
    if option == "song":
        search_type = "track"
    else:
        search_type = option

    # search spotify based on provided search arguments and search type
    try:
        resp = requests.get("https://api.spotify.com/v1/search",
                            params={"q": "+".join(args), "type": search_type,
                                    "limit": "1"},
                            headers={"Authorization": "Bearer " + access_token})
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # get and play the uri of the top result of the search
    uri = resp.json()[search_type + "s"]["items"][0]["uri"]
    if search_type == "track":
        json_body_data = json.dumps({"uris": [uri]})
    else:
        json_body_data = json.dumps({"context_uri": uri})

    try:
        resp = requests.put("https://api.spotify.com/v1/me/player/play",
                            headers={
                                "Authorization": "Bearer " + access_token},
                            data=json_body_data)
    except requests.exceptions.RequestException as exception:
        print(exception)
        sys.exit(1)

    # display which song is now playing - allow a short delay for player to begin
    # playing selected song before polling song for its metadata
    time.sleep(0.25)
    curr_song()
