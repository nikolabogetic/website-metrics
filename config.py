from configparser import ConfigParser

config_object = ConfigParser()
config_object.read('config/config.ini')
kafka_conf = config_object['KAFKA']
postgres_conf = config_object['POSTGRES']