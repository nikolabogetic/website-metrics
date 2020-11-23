import json
from kafka.admin import NewTopic
from kafka import errors
from config import kafka_conf, postgres_conf
from utils.kafka import init_admin, init_producer, init_consumer
from website_checker import collect_metrics

def test_send_receive_message():
    data = [
        {
            'url': 'https://www.wikipedia.org/',
            'status_code': 200,
            'response_time': 0.1234,
            'regex_found': True
        },
        {
            'url': 'https://www.stackoverflow.com/',
            'status_code': 500,
            'response_time': 0.1784,
            'regex_found': False
        },
        {
            'url': 'https://www.example.org/',
            'status_code': 404,
            'response_time': 0.10973,
            'regex_found': None
        },
    ]

    # Init admin, producer, consumer
    topic = 'pytest'
    kafka_conf['topic'] = topic
    admin_client = init_admin(kafka_conf)
    producer = init_producer(kafka_conf)
    consumer = init_consumer(kafka_conf)

    # Create topic
    topic_list = []
    topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=3))
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except errors.TopicAlreadyExistsError:
        pass

    # Receive any messages queued up from previous tries
    raw_msgs = consumer.poll(timeout_ms=5000)
    consumer.commit()

    # Send data
    for msg in data:
        producer.send(topic, value=msg)
    producer.flush()

    # Receive data
    received_data = []
    raw_msgs = consumer.poll(timeout_ms=2000)
    for _, msgs in raw_msgs.items():
        for msg in msgs:
            received_data.append(json.loads(msg.value))
    consumer.commit()

    assert data == received_data
