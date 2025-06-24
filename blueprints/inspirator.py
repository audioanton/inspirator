from flask import Blueprint, render_template, request, session, redirect, url_for, Response, jsonify, stream_with_context
from requests_oauthlib import OAuth2Session
from utils.inspirator_utils import generate_sound, get_search_uri, get_download_uri, Inspirator, get_mime_type
from werkzeug.utils import send_file
from dotenv import load_dotenv
import io, os

load_dotenv()
inspirator = Blueprint('inspirator', __name__, template_folder='templates', url_prefix='/inspirator')

utils = Inspirator(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])

@inspirator.route('/')
def home():
    return render_template('inspirator.html', word=utils.get_word(), types=utils.types)

@inspirator.route('/authorize')
def authorize():
    if len(request.args) == 0:
        utils.setup()
        return redirect(utils.authorization_url)

    if request.args.get('code'):
        session['token'] = utils.get_token(request.args.get('code'), utils.oauth_state)
        session['authorized'] = True

    return redirect(url_for('inspirator.home'))

@inspirator.route('/search', methods=['POST'])
def search():
    # TODO validate input

    oauth = utils.get_oauth()
    text = request.form.get('text')
    selected_types = request.form.getlist('file_types')
    max_length = request.form.get('slider')

    uri = get_search_uri(text, utils.fields, max_length)

    response = oauth.get(uri)
    if response.ok:
        utils.filter_sounds(response, selected_types)
        if len(utils.sounds) == 0:
            return render_template('inspirator.html', error='No sounds found!', types=utils.types)
        return render_template('inspirator.html', sounds=utils.get_three_sounds(), search_word=text, types=utils.types)

    return render_template('inspirator.html', error=response.status_code)

@inspirator.route('/word')
def word():
    return jsonify(utils.get_word())

@inspirator.route('/stream/<sound_id>/<type>')
def stream(sound_id, type):
    oauth = utils.get_oauth()
    result = oauth.get(get_download_uri(sound_id), stream=True)
    if result.ok:
        return Response(generate_sound(result), mimetype=get_mime_type(type))
    return 'Error'

@inspirator.route('/download/<sound_id>/<sound_name>/<type>', methods=['GET'])
def download(sound_id, sound_name, type):
    oauth = OAuth2Session(utils.client_id, token=session['token'])
    result = oauth.get(get_download_uri(sound_id), stream=True)
    if result.ok:
        file_stream = io.BytesIO(result.content)
        return send_file(file_stream, request.environ, as_attachment=True, mimetype=get_mime_type(type), download_name=sound_name)
    return f'Error (code: {result.status_code})'

@inspirator.route('/new_sounds', methods=['GET'])
def get_new_sounds():
    return jsonify(utils.get_three_sounds()).json