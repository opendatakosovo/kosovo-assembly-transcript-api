import os
import ConfigParser

from logging.handlers import RotatingFileHandler

from flask import Flask

from utils.utils import Utils

utils = Utils()


def create_app():
    ''' Create the Flask app.
    '''
    # Create the Flask app.
    app = Flask(__name__)

    # Load application configurations
    load_config(app)

    # Configure logging.
    configure_logging(app)

    # Register URL rules.
    register_url_rules(app)

    return app


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''

    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    # FIXME: Use the "common pattern" described in "Configuring from Files": http://flask.pocoo.org/docs/config/
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    # Set up config properties
    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')

    app.config['Elasticsearch'] = config.get('Elasticsearch', 'Server')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()


def configure_logging(app):
    ''' Configure the app's logging.
    :param app: The Flask app object.
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    app.logger.info('Logging to: %s', log_path)


# Import forms
from views.search_by_party import SearchByParty
from views.search_by_term import SearchByTerm


def register_url_rules(app):
    ''' Register the URL rules.
        Use pluggable class-based views: http://flask.pocoo.org/docs/views/
    :param app: The Flask application instance.
    '''

    # Count the term mentioned by party.
    app.add_url_rule(
        '/term-mentioned-by-party/<string:keyword>',
        view_func=SearchByParty.as_view('search_by_party'))

    # Term counting use by dates.
    app.add_url_rule(
        '/term-mentioned-by-date/<string:keyword>',
        view_func=SearchByTerm.as_view('search_by_term'))
