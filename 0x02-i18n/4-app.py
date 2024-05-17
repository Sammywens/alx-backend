#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
from flask_babel import Babel
from flask import Flask, render_template, request


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
    return render_template('4-index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
