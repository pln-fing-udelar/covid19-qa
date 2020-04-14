import os


class Development(object):
    """
    Development environment configuration
    """
    DEBUG = False
    TESTING = False
    API_PATH = '/core'


class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    API_PATH = os.getenv('API_PATH')


app_config = {
    'development': Development,
    'production': Production,
}
