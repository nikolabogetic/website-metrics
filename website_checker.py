import requests
import json
import re
import argparse
from config import kafka_conf
from kafka import errors
from kafka.admin import NewTopic

from utils import RepeatedTimer
from kafka_utils import init_admin, init_producer

def collect_metrics(website, pattern=None, publish=True, topic=None):
    """Retrieve metrics (status code, response time) from a given website. 
    Optionally, search for a regex pattern. Then publish to a Kafka topic.

    Arguments:
        website (str): URL of website to collect metrics from
        pattern (str, optional): Regex pattern to look for
        publish (bool, optional): Publish to a Kafka topic, default true
        topic (str, optional): Name of the Kafka topic
    Returns:
        data (dict): Key-value object with desired metrics
    """
    r = requests.get(website)

    match = None    
    # Try searching for regex pattern if provided
    if pattern and r.status_code == 200:
        match = True if re.search(pattern, r.text) else False

    data = {
        'url': website,
        'status_code': r.status_code,
        'response_time': r.elapsed.total_seconds(),
        'regex_found': match
    }
    print(data)

    if publish:
        producer.send(topic, value=data)
    return data

if __name__ == '__main__':
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
        print('Creating topic')
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except errors.TopicAlreadyExistsError:
        print('Topic already exists, skipping')
    # Start periodic collection of metrics
    rt = RepeatedTimer(int(args.time), collect_metrics, args.url, pattern=args.pattern, topic=topic)
    rt.start()
