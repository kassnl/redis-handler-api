#! coding:utf-8
'''

@author: rmuslimov
@date: 06.08.2012
@copyright (c) 2012 Directness

'''

import os
import sys

# ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.abspath(\
        os.path.split(__file__)[0]
    )))

import handlers
PROCESS='process'
BACKGROUND='background'
SEND='send'

#DEFAULT_LOG_LEVEL = 'INFO'
DEFAULT_LOG_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'formatters': {
        'extended': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%Y%m%d %H%M%S' #'datefmt': '%d %b %Y, %H:%M:%S',
        },
        'jsonf': {
            '()': 'jsonlogger.JsonFormatter',
            'fmt': '%(_id)s %(levelname)s %(asctime)s %(customer)s %(message)s %(name)s %(funcName)s %(filename)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
    },
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': DEFAULT_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'extended',
        },
        'sqs': {
            'class': 'handlers.sqshandler.SQSHandler',
            'formatter': 'jsonf',
        },
    },
    'loggers': {
        'redis_api': {
            'handlers': ['sqs'],
            'level': DEFAULT_LOG_LEVEL,
            'group': PROCESS,
            'order': 3
            },
    }
}