import pickle
import webbrowser
import requests

# relevant app information
CLIENT_ID = "bef4189e0ebb431a8ceef5b2339f498a"
CLIENT_SECRET = "93f82ef870ae48da9a8a4530ca9d82cb"
REDIRECT_URI = "http://justinawrey.github.io/spo"
SCOPES = "user-read-currently-playing user-modify-playback-state user-read-recently-played"


def checkAuthenticationStatus():
    with open("token.pk", "rb") as pickle_file:
        data = pickle.load(pickle_file)
    print(data)


def authenticate():
    # Spo follows Spotify Authorization Code Flow
    # https://developer.spotify.com/web-api/authorization-guide/

    # application requests authorization
    # this GET request must be done through browser as the web API
    # returns js to be run
    auth_req = "https://accounts.spotify.com/authorize" + \
        "?redirect_uri=" + REDIRECT_URI + \
        "&scope=" + SCOPES + \
        "&client_id=" + CLIENT_ID + \
        "&response_type=code"
    auth_req.replace(":", "%3A").replace("/", "%2F").replace(" ", "+")
    webbrowser.open(auth_req)

    # application receives authorization code
    # abort on authorization failure
    url = input("authenticate and enter URL")
    if url.find("code="):
        auth_code = url[url.find("code=") + 5:]
    else:
        print("authorization failed... aborting")
        return

    # application requests access tokens and refresh tokens
    resp = requests.post("https://accounts.spotify.com/api/token",
                         data={"grant_type": "authorization_code",
                               "redirect_uri": REDIRECT_URI,
                               "code": auth_code},
                         auth=(CLIENT_ID, CLIENT_SECRET))
    # pickle tokens so user does not have to re-authenticate
    # every time script is run
    resp_json = resp.json()
    pickle_data = {
        "access_token": resp_json["access_token"],
        "expiry": resp_json["expires_in"],
        "refresh_token": resp_json["refresh_token"],
    }
    with open("token.pk", "wb") as pickle_file:
        pickle.dump(pickle_data, pickle_file)

checkAuthenticationStatus()
