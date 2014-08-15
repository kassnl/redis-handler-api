__author__ = 'kassandracharalampidou'

import traceback
import logging
logger = logging.getLogger(name='redis_api')


class ConnectionWithRedisError(Exception):
    def __init__(self, host, port):
        self.msg = 'Redis is unreachable host:%s port:%s' % (host, port)
        logger.error('Unable to connect to Redis on %s:%s' % (host, port))
        pass

    def __str__(self):
        return self.msg

class SQSMessageSendingfFailedError(Exception):
    def __init__(self, e, region, process, action):
        self.msg = 'Failed to send SQS message'
        logger.error('Unable to send SQS message for process %s, action %s, on region %s: %s'
                                      % (process, action, region, e.args))
        pass

    def __str__(self):
        return self.msg

class ConfigurationFileNotFound(Exception):
    def __init__(self, filename):
        self.msg = 'Configuration file not found'
        logger.error('Configuration file %s not found' % filename)
        pass

    def __str__(self):
        return self.msg

class CustomerNotFoundError(Exception):
    def __init__(self, customer):
        self.msg = 'Customer %s not found' % customer
        logger.error('Customer %s not found' % customer)
        pass

    def __str__(self):
        return self.msg

class HostNotFoundError(Exception):
    def __init__(self, customer):
        self.msg = 'Host not found for customer: %s' % customer
        logger.error('Host not found for customer: %s' % customer)
        pass

    def __str__(self):
        return self.msg