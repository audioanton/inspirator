import os
from flask import Flask, render_template, request, redirect, url_for, session
from blueprints.inspirator import inspirator

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(inspirator)

links = {'home':'/', 'about':'/about/', 'contact':'/contact/', 'blog':'/blog/', 'listen':'/listen/', 'inspirator':'/inspirator/'}
social_medias = {'linkedin':'https://www.linkedin.com/in/audioanton/',
                 'facebook':'https://www.facebook.com/profile.php?id=100086758519316',
                 'youtube':'https://www.youtube.com/@audioanton'}
videos = {
    'first':('https://www.youtube-nocookie.com/embed/QyskG4EMSWo?si=a9IbJIppEFCWWM6d&amp;controls=0', 'music'),
    'second':('https://www.youtube-nocookie.com/embed/ZRly-YPk4kc?si=wld6pVLOsadNa2qx&amp;controls=0', 'music'),
    'third':('https://www.youtube-nocookie.com/embed/NYtfEE9QNEY?si=aVITRg-4xBztQCZl&amp;controls=0', 'sound design'),
    'fourth':('https://www.youtube-nocookie.com/embed/tEmxiWvpdlg?si=gMx7ZtboYrNTAfwH&amp;controls=0', 'music')
}

@app.context_processor
def inject_links():
    return dict(links=links)

@app.context_processor
def inject_social_medias():
    return dict(social_medias=social_medias)

@app.context_processor
def inject_videos():
    return dict(videos=videos)
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/listen/')
def listen():
    return render_template('listen.html')

