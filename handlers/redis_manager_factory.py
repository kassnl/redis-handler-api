__author__ = 'kassandracharalampidou'

import redis
from handlers.redis_managers.generic_manager import RedisGenericManager
from handlers.redis_managers.bounces_manager import RedisBouncesManager
from handlers.redis_managers.settings_manager import RedisSettingsManager
from handlers.redis_managers.hosts_manager import RedisHostsManager

# generic Redis connection maker. Depending on the given db, opens a different connection
class RedisManagerFactory():
    def __init__(self, settings, db):
        self.settings = settings
        self.db = db

    def get_manager(self):
        if self.db == "db_settings":
            return RedisSettingsManager(self.settings, self.db)
        if self.db == "db_rules":
            return RedisSettingsManager(self.settings, self.db)
        if self.db == "db_templates":
            return RedisSettingsManager(self.settings, self.db)
        if self.db == "db_stoplist":
            return RedisBouncesManager(self.settings, self.db)
        if self.db == "db_bounces":
            return RedisBouncesManager(self.settings, self.db)
        if self.db == "db_hosts":
            return RedisHostsManager(self.settings, self.db)

