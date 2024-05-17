#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
import pytz
from flask_babel import Babel, format_datetime
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
    'Accept-Language' header or from the user's preferred locale or from the
    'locale' parameter in the request's query string.

    Returns:
        str: The selected language code or None if no matching language found.
    """
    # Check if 'locale' parameter is present in the request's query string
    if 'locale' in request.args:
        locale = request.args.get('locale')
        # Check if the provided locale is one of the supported languages
        if locale in app.config['LANGUAGES']:
            return locale

    # Check if the user is logged in and has a preferred locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # Fallback to the best-matching language from the request's
    # 'Accept-Language' header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the best-matching time zone from the
    request's 'timezone' parameter or from the
    user's preferred time zone or use the default timezone (UTC).

    Returns:
        str: The selected time zone or None
        if no matching or valid time zone found.
    """
    # Check if 'timezone' parameter is present in the request's query string
    if 'timezone' in request.args:
        timezone = request.args.get('timezone')
        try:
            # Validate the provided time zone using pytz.timezone
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Check if the user is logged in and has a preferred time zone
    if g.user and g.user.get('timezone'):
        try:
            # Validate the user's preferred time zone using pytz.timezone
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Fallback to the default time zone (UTC)
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index_value() -> str:
    """
    Render the index.html template.

    Returns:
        str: The rendered HTML content.
    """
    g.time = format_datetime()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
