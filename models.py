#! coding:utf-8

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CustomerList(Base):
    __tablename__ = 'cgcore_companies'

    id = sa.Column(sa.Integer, primary_key=True)
    company_name = sa.Column(sa.String(length=360), default='', nullable=False)
    secure_word = sa.Column(sa.String(length=360), default='', nullable=False)
    mysql_server = sa.Column(sa.Integer, nullable=False)
    mysql_username = sa.Column(sa.String(length=50), nullable=False)
    mysql_password = sa.Column(sa.String(length=50), nullable=False)
    mysql_database = sa.Column(sa.String(length=50), nullable=False)
    package = sa.Column(sa.String(length=20), nullable=False)
    s3_bucket = sa.Column(sa.String(length=15), nullable=False)
    agent_login = sa.Column(sa.Boolean, nullable=False)
    ip_lock = sa.Column(sa.Boolean, nullable=False)
    mail_report = sa.Column(sa.Boolean, default=False, nullable=False)
    google_translate = sa.Column(sa.Boolean, nullable=False)
    salesforce = sa.Column(sa.Boolean, nullable=False)
    sms = sa.Column(sa.Boolean, nullable=False)
    summary = sa.Column(sa.Boolean, nullable=False)
    open_dashboard = sa.Column(sa.Boolean, nullable=False)
    alias = sa.Column(sa.String(length=120), nullable=False)
    data_model = sa.Column(sa.Text(assert_unicode=True))


class Database(Base):
    __tablename__ = 'cgcore_dbs'

    id = sa.Column(sa.Integer, primary_key=True)
    main_server = sa.Column(sa.String(length=255), nullable=False)
    main_location = sa.Column(sa.String(length=20), nullable=False)
    settings = sa.Column(sa.Text(assert_unicode=True))
