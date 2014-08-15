#!
__author__ = 'kassandracharalampidou'

from datetime import datetime
from models import CustomerList, Database
from helpers import safe_session, autoconnect
import sqlalchemy as sa
import copy

# WHEN POSTING, WORK WITH POST_PER_LOC RECORDS
POST_PER_LOCK = 10


class DBManagerFactory():
    def __init__(self, settings, rds_name, db_name=None):
        self.settings = settings
        self.rds_name = rds_name
        self.db_name = db_name

    def get_manager(self):
        engine, session = autoconnect(dict(self.settings.items(self.rds_name)), self.db_name)
        if self.rds_name == "GLOBAL_DB":
            return GlobalDBManager(session, engine)
        return None

class AbstractDBManager():
    '''
    Manages queries from the db and injects results to procedures that need them
    '''
    @safe_session
    def __init__(self, session, engine):
        self.session = session
        self.engine = engine

    def db_flush(self):
        self.session.flush()

    def db_commit(self):
        self.session.commit()


class GlobalDBManager(AbstractDBManager):
    def get_host(self, customer):
        company = self.session.query(CustomerList).filter_by(mysql_database = customer).first()
        if company:
            host = self.session.query(Database).filter_by(id=company.mysql_server).first()
            if host:
                return host.main_server
        return None


