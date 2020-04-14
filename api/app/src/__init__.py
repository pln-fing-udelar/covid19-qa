import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Namespace

from .config import app_config

app = Flask('covid-19')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config.from_object(app_config[os.getenv('FLASK_ENV')])
api = Api(app,
          version='0.1',
          title='Covid19 QA Api',
          description='Covid19 QA Api '
          )

ns_covid_qa = Namespace('Covid19-QA', description='QA Operations')
api.add_namespace(ns_covid_qa)
ns_test = Namespace('Covid19-Test', description='Test Operations')
api.add_namespace(ns_test)

if app_config[os.getenv('FLASK_ENV')].DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
