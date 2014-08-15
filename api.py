#!flask/bin/python
__author__ = 'kassandracharalampidou'
from handlers.redis_manager_factory import RedisManagerFactory
from settings.constants import SettingsGenerator
from logging_settings import LOGGING
from logging.config import dictConfig
from api_responses import RESPONSE_CODE
from api_exceptions import ConfigurationFileNotFound, CustomerNotFoundError, ConnectionWithRedisError, HostNotFoundError
from handlers.data_manager import DataManager
from handlers.redis_manager_factory import RedisManagerFactory
from handlers.db_manager import DBManagerFactory

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask app running!"

@app.route('/api/redis/clean_templatewhere/<customer_name>', methods = ['GET'])
def clean_templatewhere(customer_name):
    try:
        settings = SettingsGenerator().__call__()
    except ConfigurationFileNotFound:
        return jsonify({'response': RESPONSE_CODE['CONF_ERROR']}), 200

    hosts = DataManager(RedisManagerFactory(settings, 'db_hosts').get_manager(),
                        DBManagerFactory(settings, "GLOBAL_DB").get_manager())
    try:
        host_name = hosts.get_customer_host(customer_name)
    except HostNotFoundError:
        return jsonify({'response': RESPONSE_CODE['HOST_NOT_FOUND']}), 200
    handler = RedisManagerFactory(settings, 'db_rules').get_manager()
    try:
        handler.flush_templatewhere(host_name, customer_name)
    except CustomerNotFoundError:
        return jsonify({'response': RESPONSE_CODE['CLIENT_NOT_FOUND']}), 200
    except ConnectionWithRedisError:
        return jsonify({'response': RESPONSE_CODE['REDIS_ERROR']}), 200
    return jsonify({'response': RESPONSE_CODE['SUCCESS']}), 200


if __name__ == '__main__':
    dictConfig(LOGGING)
    app.run(debug = True, host='0.0.0.0')