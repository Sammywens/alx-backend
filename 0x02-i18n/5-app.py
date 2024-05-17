#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
from flask_babel import Babel
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user(user_id) -> Union[Dict, None]:
    """
    Get user details from the user table by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict or None: The user dictionary or None if user ID not found.
    """
    return users.get(user_id)

@app.before_request
def before_request() -> None:
    """
    Executed before all other functions to set the
    current user in flask.g.user.
    """
    g.user = None
    login_as = int(request.args.get('login_as', 0))
    if login_as > 0:
        g.user = get_user(login_as)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best-matching language from the request's
    'Accept-Language' header
    or from the 'locale' parameter in the request's query string.

    Returns:
        str: The selected language code or
        None if no matching language found.
    """
    # Check if 'locale' parameter is present in the request's query string
    if 'locale' in request.args:
        locale = request.args.get('locale')
        # Check if the provided locale is one of the supported languages
        if locale in app.config['LANGUAGES']:
            return locale

    # If the 'locale' parameter is not present or not supported,
    # use default behavior
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Render the index.html template.

    Returns:
        str: The rendered HTML content.
    """
    return render_template('5-index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
