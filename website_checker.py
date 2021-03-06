import json
import logging
import sys
from kafka import errors
from kafka.admin import NewTopic

from config import conf
from utils.web import collect_metrics
from utils.timer import RepeatedTimer
from utils.kafka import init_admin, init_producer


def collect_and_publish(website, topic, pattern=None):
    try:
        data = collect_metrics(website, pattern)
    except ValueError as e:
        logger.error('Invalid value provided.')
        logger.error(e)
        sys.exit(1)
    logger.info(data)
    producer.send(topic, value=data)
    return


if __name__ == '__main__':
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    logger.info('Website checker started')

    # Create Kafka admin and producer, get topic name from config
    try:
        admin_client = init_admin(conf)
        producer = init_producer(conf)
    except errors.KafkaError as e:
        logger.error('Kafka error:')
        logger.error(e)
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(e)
        logger.error('Check that Kafka certificate files are in ./cert/')
        sys.exit(1)

    # Create new topic
    topic_list = []
    topic_list.append(NewTopic(name=conf.kafka_topic, num_partitions=1, replication_factor=3))
    try:
        logger.info('Creating topic')
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except errors.TopicAlreadyExistsError:
        logger.info('Topic already exists, skipping')
    # Start periodic collection of metrics
    rt = RepeatedTimer(int(conf.interval), collect_and_publish, conf.website, conf.kafka_topic, pattern=conf.pattern)
    try:
        rt.start()
        while True:
            pass
    except KeyboardInterrupt:
        logger.error('Keyboard interrupt - closing connection')
        rt.stop()

