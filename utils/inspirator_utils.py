import requests
import random
from flask import session, jsonify
from requests_oauthlib import OAuth2Session
import re

class Inspirator:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://freesound.org/apiv2/oauth2/access_token/"
        self.types = ['wav', 'mp3', 'ogg', 'flac']
        self.fields = 'name,id,type,duration,filesize,bitrate,samplerate'
        self.words = get_words()
        self.max_length = 3
        self.authorization_url = ''
        self.oauth_state = ''
        self.sounds = []

    def setup(self):
        oauth = OAuth2Session(self.client_id)

        self.authorization_url, self.oauth_state = oauth.authorization_url(
            "https://freesound.org/apiv2/oauth2/authorize/"
        )

    def get_token(self, code, state):
        oauth = OAuth2Session(self.client_id, state=state)
        token = oauth.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code
        )
        return token

    def get_oauth(self):
        return OAuth2Session(self.client_id, token=session['token'])

    def set_max_length(self, length):
        self.max_length = length

    def get_word(self):
        return self.words.pop(random.randint(0, len(self.words) - 1))

    def filter_sounds(self, response, types):
        results = jsonify(response.json()).json['results']

        self.sounds = [(sound['id'], sound['name'], sound['type'], round(sound['duration'], 1),
                        round(sound['filesize'] / 1_000_000, 2)) for
                       sound in results if sound['type'] in types]

    def get_sound(self):
        return self.sounds.pop(random.randint(0, len(self.sounds) - 1))

    def get_three_sounds(self):
        sounds = []
        for number in range(3):
            if len(self.sounds) > 0:
                sounds.append(self.get_sound())
        return sounds


def generate_sound(response):
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            yield chunk

def get_search_uri(query, fields, max_length):
    return f"https://freesound.org/apiv2/search/text/?query={query}&filter={get_duration(max_length)}&fields={fields}"

def get_duration(max_length):
    return f'duration:[* TO {max_length}]'

def get_download_uri(sound_id):
    return f'https://freesound.org/apiv2/sounds/{sound_id}/download/'

def get_words():
    pattern = 'sports|animals|birds|games|softwares|countries|capitals_of_countries'
    response = requests.get('https://random-words-api.kushcreates.com/api', params=[('language', 'en')])
    if response.ok:
        filtered = [word for word in response.json() if re.search(pattern, word['category']) and len(word['word'].split()) == 1]
        words = [word['word'] for word in filtered]
        return words

def get_mime_type(file_type):
    return f'audio/{file_type}'

def validate_file_types(selected_types, accepted_types):
    if len(selected_types) <= 0:
        return False

    for file_type in selected_types:
        if file_type not in accepted_types:
            return False

    return True
