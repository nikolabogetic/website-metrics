from database_writer import create_metrics_table, insert_data
from utils import init_postgres
from config import postgres_conf


def test_database_writer():
    conn = init_postgres(postgres_conf)
    data = {
        'url': 'https://www.wikipedia.org/',
        'response_time': 0.10382,
        'status_code': 200,
        'regex_found': True
    }
    create_metrics_table(conn)
    insert_data(conn, data)
    with conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT * FROM website_metrics ORDER BY timestamp DESC LIMIT 1;
                """
            )
            row = curs.fetchone()
            assert row[1] == data.get('url')
            assert row[2] == data.get('response_time')
            assert row[3] == data.get('status_code')
            assert row[4] == data.get('regex_found')