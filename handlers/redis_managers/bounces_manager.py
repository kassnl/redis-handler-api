__author__ = 'kassandracharalampidou'
from handlers.redis_managers.generic_manager import RedisGenericManager, safe_redis_connection

class RedisBouncesManager(RedisGenericManager):
    @safe_redis_connection
    def flush_bounces(self):
        self.rc.flushdb()
