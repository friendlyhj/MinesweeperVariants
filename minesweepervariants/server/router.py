from flask import Flask, redirect
from flask_cors import CORS

from .config import CORS_resources, github_web
from .model import generate_board, metadata, click, hint_post, get_rule_list, reset

__all__ = ["app"]

app = Flask(__name__)
CORS(app, resources=CORS_resources)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Referrer-Policy'] = 'unsafe-url'
    if 'Access-Control-Allow-Credentials' in response.headers:
        try:
            del response.headers['Access-Control-Allow-Credentials']
        except Exception:
            pass
    return response

@app.route('/')
def root():
    return redirect(github_web)

app.add_url_rule('/api/new', 'generate_board', generate_board, methods=['GET', 'POST'])
app.add_url_rule('/api/metadata', 'metadata', metadata, methods=['GET', 'POST'])
app.add_url_rule('/api/click', 'click', click, methods=['GET', 'POST'])
app.add_url_rule('/api/hint', 'hint_post', hint_post, methods=['GET', 'POST'])
app.add_url_rule('/api/rules', 'get_rule_list', get_rule_list, methods=['GET', 'POST'])
app.add_url_rule('/api/reset', 'reset', reset, methods=['GET', 'POST'])