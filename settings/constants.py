#! coding:utf-8
'''
Defines settings according to EC2 User Data or input file
@author: kcharalampidou
@date: 14.04.2014
@copyright (c) 2014 Directness

'''

import os
import json
import urllib2
import ConfigParser
import __root__
from api_exceptions import ConfigurationFileNotFound

USER_DATA_URL = "http://169.254.169.254/latest/user-data/"
CONFIG_DIR = "settings/conf/"
SETTINGS_FILENAME = "settings.conf"
US_ZONE = "us-east-1d"
EU_ZONE = "eu-west-1a"
AUS_ZONE = "ap-southeast-2a"


class SettingsGenerator:
    def __call__(self, json_file = None):
        config = ConfigParser.RawConfigParser()
        # Checks if the settings settings file already exists
        if os.path.isfile(os.path.join(__root__.path(), CONFIG_DIR + SETTINGS_FILENAME)):
            config.read(CONFIG_DIR + SETTINGS_FILENAME)
            return config
        # Reads the EC2 User Data file
        user_data = self.fetch_ec2_user_data(json_file)
        # Checks if file contains the needed information
        system_specs = self.parse_user_data(user_data)
        # Returns settings according to system specs
        return self.retrieve_constants(system_specs)


    def fetch_ec2_user_data(self, json_file):
        '''
        Reads the given json file or USER_DATA_URL
        '''
        if json_file:
            with open(json_file) as fp:
                try:
                    user_data = json.load(fp)
                except ValueError, e:
                    raise Exception('Unable to parse file %s' %json_file)
        else:
            with urllib2.urlopen(USER_DATA_URL) as fp:
                try:
                    user_data = json.load(fp)
                except ValueError, e:
                    raise Exception('Unable to parse EC2 user data json file')
        return user_data


    def parse_user_data(self, user_data):
        '''
        Checks EC2 User Data
        '''
        specs = {}
        if user_data['customergauge-instance']:
            if 'type' in user_data['customergauge-instance']:
                specs['type'] = user_data['customergauge-instance']['type']
            else:
                raise Exception('System type [dev/prod] not defined')

            if 'role' in user_data['customergauge-instance']:
                specs['role'] = user_data['customergauge-instance']['role']
            else:
                raise Exception('System role [processor/outbox/listener] not defined')

            if 'zone' in user_data['customergauge-instance']:
                specs['zone'] = user_data['customergauge-instance']['zone']
            else:
                raise Exception('System zone [US/EUR/AUS] not defined')
            return specs
        else:
            raise Exception('Instance properties not defined')


    def retrieve_constants(self, system_specs):
        '''
        Returns settings according to system specifications
        '''
        config = ConfigParser.RawConfigParser()
        conf_filename = system_specs['type']+ '-' + system_specs['zone'] + '.conf'
        if not os.path.isfile(CONFIG_DIR + conf_filename):
            raise ConfigurationFileNotFound(conf_filename, "MailExpress")
        config.read(CONFIG_DIR + conf_filename)
        for f in os.listdir(CONFIG_DIR):
          os.remove(CONFIG_DIR + f)
        with open(CONFIG_DIR + SETTINGS_FILENAME, 'wb') as configfile:
          config.write(configfile)
        configfile.close()
        return config
        # Add more cases here
