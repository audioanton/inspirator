import os
from flask import Flask, redirect, url_for
from blueprints.inspirator import inspirator

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(inspirator)

# links = {'home':'/', 'about':'/about/', 'contact':'/contact/', 'blog':'/blog/', 'listen':'/listen/', 'inspirator':'/inspirator/'}
social_medias = {'linkedin':'https://www.linkedin.com/in/audioanton/',
                 'facebook':'https://www.facebook.com/profile.php?id=100086758519316',
                 'youtube':'https://www.youtube.com/@audioanton'}

# @app.context_processor
# def inject_links():
#     return dict(links=links)

@app.context_processor
def inject_social_medias():
    return dict(social_medias=social_medias)

@app.route('/')
def index():
    return redirect(url_for('inspirator.home'))

