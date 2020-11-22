import psycopg2
import json

from config import kafka_conf, postgres_conf
from utils import init_postgres
from kafka_utils import init_consumer

def create_metrics_table(connection):
    """Create table to store metrics in Postgres. 
    Adds automatic timestamp on insert (UTC time). 

    Arguments:
        connection (obj): Postgres connection object returned by psycopg2.connect
    """
    with connection:
        with connection.cursor() as curs:
            curs.execute(
                """
                CREATE TABLE IF NOT EXISTS website_metrics (
                    timestamp timestamp default current_timestamp,
                    url varchar not null,
                    response_time real not null,
                    response_code int not null,
                    regex_found bool
                );        
                """
            )
    return

def insert_data(connection, data):
    """Insert collected metrics data into Postgres table. 
    
    Arguments:
        connection (obj): Database connection object returned by psycopg2.connect
        data (dict): Key-value object with desired metrics 
    """
    with connection:
        with connection.cursor() as curs:
            curs.execute(
                """
                INSERT INTO website_metrics (url, response_time, response_code, regex_found)
                VALUES (%s, %s, %s, %s);
                """,
                (data.get('url'), data.get('response_time'), data.get('status_code'), data.get('regex_found'))
            )
    return


if __name__ == '__main__':
    # Create Kafka consumer and Postgres connection
    consumer = init_consumer(kafka_conf)
    conn = init_postgres(postgres_conf)

    try:
        create_metrics_table(conn)
        # Loop trhough Kafka messages
        for msg in consumer:
            record = json.loads(msg.value)
            print('Received: {}'.format(record.get('status_code')))
            insert_data(conn, record)
    except psycopg2.Error as error:
        print('Postgres error', error)
    except KeyboardInterrupt:
        print('Keyboard interrupt - waiting until connection is closed')
    except:
        print('Unhandled exception')
    finally:
        conn.close()

