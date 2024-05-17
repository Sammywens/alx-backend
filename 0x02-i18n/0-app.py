#!/usr/bin/env python3
"""
A basic flask app
"""

from flask import Flask, render_template

app: Flask = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index_value() -> str:
    """
    Render the index.html template.

    Returns:
        str: The rendered HTML content.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
