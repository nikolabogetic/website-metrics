import json
import os
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient

from config import certpath


def init_admin(conf):
    """Initialize Kafka Admin connection with parameters from the config object.

    Arguments:
        conf (obj): Config object with loaded environment variables
    Returns:
        admin_client (obj): Kafka Admin client object
    """
    admin_client = KafkaAdminClient(
        bootstrap_servers=conf.kafka_uri,
        security_protocol='SSL',
        ssl_cafile=certpath+'ca.pem',
        ssl_certfile=certpath+'service.cert',
        ssl_keyfile=certpath+'service.key',
        client_id='website-checker'
    )
    return admin_client


def init_producer(conf):
    """Initialize Kafka Producer with parameters from the config object.

    Arguments:
        conf (obj): Config object with loaded environment variables
    Returns:
        producer (obj): Kafka Producer object
    """
    producer = KafkaProducer(
        bootstrap_servers=conf.kafka_uri,
        security_protocol='SSL',
        ssl_cafile=certpath+'ca.pem',
        ssl_certfile=certpath+'service.cert',
        ssl_keyfile=certpath+'service.key',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer


def init_consumer(conf):
    """Initialize Kafka Consumer with parameters from the config object.

    Arguments:
        conf (obj): Config object with loaded environment variables
    Returns:
        consumer (obj): Kafka Consumer object
    """
    consumer = KafkaConsumer(
        conf.kafka_topic,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        bootstrap_servers=conf.kafka_uri,
        client_id='database-writer-1',
        group_id='database-writers',
        security_protocol='SSL',
        ssl_cafile=certpath+'ca.pem',
        ssl_certfile=certpath+'service.cert',
        ssl_keyfile=certpath+'service.key',
    )
    return consumer


