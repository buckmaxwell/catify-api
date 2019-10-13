from flask import Flask, jsonify, request
from requests.auth import HTTPBasicAuth
import arrow
import os
import psycopg2
import requests

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_STATE = 'prevent_cross_site_request_forgery55'
SPOTIFY_REDIRECT_URI = 'http://167.99.7.55:5000/spotify'

SPOTIFY_API_SCOPES = [
        'playlist-modify-private',
        'playlist-modify-public',
        'playlist-read-collaborative',
        'playlist-read-private',
        'user-library-modify',
        'user-library-read',
        'user-read-recently-played',
        'user-top-read',
        ]

app = Flask(__name__)




def spotify_request_tokens(code):
    resp = requests.post('https://accounts.spotify.com/api/token',
            data = {
                'grant_type': "authorization_code",
                'code': code,
                'redirect_uri': SPOTIFY_REDIRECT_URI
                },
            auth = HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
            )
    if resp.status_code == 200:
        access = resp.json['access_token']
        scope = resp.json['scope']
        expires = arrow.now().shift(resp.json['expires_in'])
        refresh = resp.json['refresh_token']
        # TODO: pick up here
        spotify_get_user_profile(access_token)
    else:
        pass


@app.route('/')
def index():

    requests.get('https://accounts.spotify.com/authorize',
        params = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'state': SPOTIFY_STATE,
            'scope': ' '.join(SPOTIFY_API_SCOPES),
            'show_dialog': 'false'
            }
        )

@app.route('/spotify')
def spotify():
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    if code is not None and state == SPOTIFY_STATE:
        spotify_request_tokens(code)
        pass
    else:
        # print error
        pass

    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)