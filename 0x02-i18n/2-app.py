#!/usr/bin/env python3
"""A Basic Flask app.
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
    'Accept-Language' header.

    Returns:
        str: The selected language code or None
        if no matching language found.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index_value() -> str:
    """
    Render the index.html template.

    Returns:
        str: The rendered HTML content.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
