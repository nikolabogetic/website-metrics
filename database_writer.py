import psycopg2
import json
import logging

from config import kafka_conf, postgres_conf
from utils.postgres import init_postgres, create_metrics_table, insert_data
from utils.kafka import init_consumer


if __name__ == '__main__':
    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    # Create Kafka consumer and Postgres connection
    consumer = init_consumer(kafka_conf)
    conn = init_postgres(postgres_conf)

    try:
        create_metrics_table(conn)
        # Loop trhough Kafka messages
        for msg in consumer:
            record = json.loads(msg.value)
            logger.debug('Received: {}'.format(record.get('status_code')))
            insert_data(conn, record)
    except psycopg2.Error as e:
        logger.error('Postgres error:')
        logger.error(e)
    except KeyboardInterrupt:
        logger.error('Keyboard interrupt - closing connection')
    except e:
        logger.error('Unhandled exception:')
        logger.error(e)
    finally:
        conn.close()

