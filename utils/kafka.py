import json
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient

certpath = 'config/certs/'


def init_admin(config):
    """Initialize Kafka Admin connection with parameters from the config object.

    Arguments:
        config (obj): Config object from the Kafka section of the config.ini file
    Returns:
        admin_client (obj): Kafka Admin client object
    """
    admin_client = KafkaAdminClient(
        bootstrap_servers=config['servers'],
        security_protocol='SSL',
        ssl_cafile=certpath+'ca.pem',
        ssl_certfile=certpath+'service.cert',
        ssl_keyfile=certpath+'service.key',
        client_id='website-checker'
    )
    return admin_client


def init_producer(config):
    """Initialize Kafka Producer with parameters from the config object.

    Arguments:
        config (obj): Config object from the Kafka section of the config.ini file
    Returns:
        admin_client (obj): Kafka Producer object
    """
    producer = KafkaProducer(
        bootstrap_servers=config['servers'],
        security_protocol='SSL',
        ssl_cafile=certpath+'ca.pem',
        ssl_certfile=certpath+'service.cert',
        ssl_keyfile=certpath+'service.key',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer


def init_consumer(config):
    """Initialize Kafka Consumer with parameters from the config object.

    Arguments:
        config (obj): Config object from the Kafka section of the config.ini file
    Returns:
        admin_client (obj): Kafka Consumer object
    """
    consumer = KafkaConsumer(
        config['topic'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        bootstrap_servers=config['servers'],
        client_id='database-writer-1',
        group_id='database-writers',
        security_protocol='SSL',
        ssl_cafile=certpath+'ca.pem',
        ssl_certfile=certpath+'service.cert',
        ssl_keyfile=certpath+'service.key',
    )
    return consumer


