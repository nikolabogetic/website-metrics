import psycopg2
import json
import logging
import sys
from kafka import errors

from config import conf
from utils.postgres import init_postgres, create_metrics_table, insert_data
from utils.kafka import init_consumer


if __name__ == '__main__':
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    logger.info('Database writer started')

    try:
        # Create Kafka consumer and Postgres connection
        consumer = init_consumer(conf)
        conn = init_postgres(conf)

        create_metrics_table(conn)
        # Loop trhough Kafka messages
        for msg in consumer:
            record = json.loads(msg.value)
            logger.info('Received: {}'.format(record.get('status_code')))
            insert_data(conn, record)

    except psycopg2.Error as e:
        logger.error('Postgres error:')
        logger.error(e)
    except errors.KafkaError as e:
        logger.error('Kafka error:')
        logger.error(e)
    except KeyboardInterrupt:
        logger.error('Keyboard interrupt - closing connection')
        conn.close()
