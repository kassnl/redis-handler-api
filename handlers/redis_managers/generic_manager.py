__author__ = 'kassandracharalampidou'
import redis
from settings.constants import SettingsGenerator
from api_exceptions import ConnectionWithRedisError

# Safe Redis connection decorator
def safe_redis_connection(func):
    def check_connection(self, *args, **kwargs):
        try:
            self.rc.ping()
        except redis.ConnectionError:
            raise ConnectionWithRedisError(self.settings.get('REDIS','host'),
                                            self.settings.getint('REDIS','port'))
        return func(self, *args, **kwargs)
    return check_connection

class RedisGenericManager():
    def __init__(self, settings, db):

        self.settings = settings
        self.db = db
        self.rc = redis.StrictRedis(host=settings.get('REDIS', 'host'),
                                    port=settings.getint('REDIS', 'port'),
                                    db=settings.getint('REDIS', db))

    @safe_redis_connection
    def get_value(self, var):
        return self.rc.get(var)

    @safe_redis_connection
    def set_value(self, var, value):
        out = self.rc.set(var, value)
        self.rc.expire(var, self.settings.getint('REDIS', 'expire_time'))
        return out

    @safe_redis_connection
    def get_hash(self, var):
        return self.rc.hgetall(var)

    @safe_redis_connection
    def set_hash(self, var, mydict):
        out = self.rc.hmset(var, mydict)
        self.rc.expire(var, self.settings.getint('REDIS', 'expire_time'))
        return out

    def implode(self, list_to_concat, delim = ":"):
        return delim.join(list_to_concat)