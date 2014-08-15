__author__ = 'kassandracharalampidou'
from handlers.redis_managers.generic_manager import RedisGenericManager, safe_redis_connection
from api_exceptions import CustomerNotFoundError

class RedisSettingsManager(RedisGenericManager):
    @safe_redis_connection
    def flush_templatewhere(self, host_name, customer_name):
        alias = "templatewhere"
        if not self.rc.exists(self.implode([host_name, customer_name, alias])):
            raise CustomerNotFoundError(customer_name)
        self.rc.delete(self.implode([host_name, customer_name, alias]))

