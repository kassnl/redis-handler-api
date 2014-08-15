__author__ = 'kassandracharalampidou'

import logging
import logging.handlers
import boto
import uuid
import json
import datetime
import time

from boto.sqs.message import RawMessage
from settings.constants import SettingsGenerator

class SQSHandler(logging.Handler):
    ''' A Python logging handler which sends messages to Amazon SQS. '''
    def __init__(self):
        logging.Handler.__init__(self)
        settings = SettingsGenerator().__call__()
        conn = boto.sqs.connect_to_region(settings.get('SQS', 'region'),
                                          aws_access_key_id=settings.get('SQS', 'access_key_id'),
                                          aws_secret_access_key=settings.get('SQS', 'secret_access_key'))
        self.q = conn.get_queue(settings.get('SQS', 'queue_log'))

    def emit(self, record):
        if isinstance(record.args, dict):
            record.customer = record.args['customer']
        else:
            record.customer = 'Sender'

        #formatted_record = self.format(record)
        ct = '%Y/%m/%d %H:%M:%S'
        dtime = datetime.datetime.utcfromtimestamp(record.created)

        data = {}
        data['levelname'] = record.levelname
        data['asctime'] = dtime.strftime(ct)
        data['customer'] = record.customer
        data['message'] = record.msg
        data['name'] = record.name
        data['funcName'] = record.funcName
        data['filename'] = record.filename
        data['@timestamp'] = datetime.datetime.strptime(data['asctime'], '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')

        msg = {}
        msg['_id'] = str(uuid.uuid4())
        msg['_index'] = "sqs-river-" + datetime.datetime.now().strftime("%Y.%m")
        msg['_type'] = "mailexpress"
        msg['_data'] = data

        #print json.dumps(msg)
        m = RawMessage()
        m.set_body(json.dumps(msg))
        self.q.write(m)
