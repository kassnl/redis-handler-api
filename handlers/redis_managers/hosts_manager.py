__author__ = 'kassandracharalampidou'
from handlers.redis_managers.generic_manager import RedisGenericManager, safe_redis_connection

class RedisHostsManager(RedisGenericManager):
    @safe_redis_connection
    def get_host(self, customer):
        if self.rc.exists(customer):
            return self.rc.get(customer)
        return False

    @safe_redis_connection
    def set_host(self, customer, host):
        return self.rc.set(customer, host)
