import os
from dotenv import load_dotenv

basedir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    def __init__(self):
        self.pg_user = os.getenv('POSTGRES_USER')
        self.pg_pass = os.getenv('POSTGRES_PASSWORD')
        self.pg_host = os.getenv('POSTGRES_HOST')
        self.pg_port = os.getenv('POSTGRES_PORT')
        self.pg_db = os.getenv('POSTGRES_DB')

        self.kafka_uri = os.getenv('KAFKA_URI')
        self.kafka_topic = os.getenv('KAFKA_TOPIC') or 'website-metrics'

conf = Config()