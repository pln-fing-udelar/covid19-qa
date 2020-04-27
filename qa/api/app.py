from datetime import datetime
from logging.config import dictConfig

import pytz
from flask import Flask
from flask_restx import Api

dictConfig({
    "version": 1,
    "formatters": {"default": {
        "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    }},
    "handlers": {"wsgi": {
        "class": "logging.StreamHandler",
        "stream": "ext://flask.logging.wsgi_errors_stream",
        "formatter": "default"
    }},
    "root": {
        "level": "DEBUG",
        "handlers": ["wsgi"]
    }
})


def create_app() -> Flask:
    datetime.now(tz=pytz.timezone("America/Montevideo"))

    app = Flask("covid-19")

    api = Api(app, version="0.1", title="COVID19-QA API", description="COVID19-QA API")

    # We import here so the model creation doesn't occur when just importing this module file but when creating the app.
    from .views import api as ns_qa
    api.add_namespace(ns_qa)

    return app
