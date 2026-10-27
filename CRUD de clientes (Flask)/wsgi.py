"""Ponto de entrada do servidor (gunicorn wsgi:app) e do modo de desenvolvimento."""

import os

from adonai import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,
            debug=os.environ.get("FLASK_DEBUG") == "1")