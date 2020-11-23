import json
from kafka.admin import NewTopic
from kafka import errors
from config import conf
from utils.kafka import init_admin, init_producer, init_consumer

def test_send_receive_message():

    data = [
        {
            'url': 'https://www.wikipedia.org/',
            'response_time': 0.1234,
            'status_code': 200,
            'regex_found': True
        },
        {
            'url': 'https://www.stackoverflow.com/',
            'response_time': 0.1784,
            'status_code': 500,
            'regex_found': False
        },
        {
            'url': 'https://www.example.org/',
            'response_time': 0.10973,
            'status_code': 404,
            'regex_found': None
        },
    ]

    # Init admin, producer, consumer
    topic = 'pytest'
    test_conf = conf
    test_conf.kafka_topic = topic
    admin_client = init_admin(test_conf)
    producer = init_producer(test_conf)
    consumer = init_consumer(test_conf)

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
