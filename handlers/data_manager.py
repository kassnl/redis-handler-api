__author__ = 'kassandracharalampidou'
from api_exceptions import ConnectionWithRedisError, HostNotFoundError

class DataManager():
    # Gets data from Redis, if up and having it, and otherwise from Database

    def __init__(self, redis_manager, db_manager):
        self.rc = redis_manager
        self.db = db_manager

    def get_customer_host(self, customer):
        # read from redis
        host = None
        try:
            host = self.rc.get_host(customer)
        except ConnectionWithRedisError:
            pass
        if not host:
            host = self.db.get_host(customer)
            if host:
                try:
                    self.rc.set_host(customer, host)
                except ConnectionWithRedisError:
                    pass
            else:
                raise HostNotFoundError(customer)
        return host
