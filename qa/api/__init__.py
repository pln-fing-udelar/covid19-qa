import logging
import os

from flask import Flask
from flask_restx import Api, Namespace

from covid19_qa.pipeline import create_qa_pipeline
from .config import app_config

app = Flask('covid-19')
app.config.from_object(app_config[os.getenv('FLASK_ENV')])
api = Api(app,
          version='0.1',
          title='Covid19 QA Api',
          description='Covid19 QA Api '
          )
ns_covid_qa = Namespace('Covid19-QA', description='QA Operations')
api.add_namespace(ns_covid_qa)

# FIXME: pass the device as a parameter of the container
qa_pipeline = create_qa_pipeline(device=os.environ.get('DEVICE', -1))


if app_config[os.getenv('FLASK_ENV')].DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
