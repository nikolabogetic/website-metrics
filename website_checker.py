import json
import argparse
import logging
from kafka import errors
from kafka.admin import NewTopic

from config import kafka_conf
from utils.web import collect_metrics
from utils.timer import RepeatedTimer
from utils.kafka import init_admin, init_producer


def collect_and_publish(website, topic, pattern=None):
    data = collect_metrics(website, pattern)
    logger.info(data)
    producer.send(topic, value=data)


if __name__ == '__main__':
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Metrics collector')
    parser.add_argument('-t', '--time', help='Time interval in seconds', required=True)
    parser.add_argument('--url', help='URL of website to scrape', required=True)
    parser.add_argument('--pattern', help='Regex pattern to look for', required=False)
    args = parser.parse_args()

    # Create Kafka admin and producer, get topic name from config
    admin_client = init_admin(kafka_conf)
    producer = init_producer(kafka_conf)
    topic = kafka_conf['topic']

    # Create new topic
    topic_list = []
    topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=3))
    try:
        logger.info('Creating topic')
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except errors.TopicAlreadyExistsError:
        logger.info('Topic already exists, skipping')
    # Start periodic collection of metrics
    rt = RepeatedTimer(int(args.time), collect_and_publish, args.url, topic, pattern=args.pattern)
    rt.start()
