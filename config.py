import os
from configparser import ConfigParser

app_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(app_root, 'config/config.ini')

config_object = ConfigParser()
config_object.read(config_path)
kafka_conf = config_object['KAFKA']
postgres_conf = config_object['POSTGRES']