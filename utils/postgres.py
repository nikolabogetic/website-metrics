import psycopg2


def init_postgres(conf):
    """Initialize Postgres connection with parameters from the config object.

    Arguments:
        conf (obj): Config object with loaded environment variables
    Returns:
        conn (obj): Postgres connection object
    """
    conn = psycopg2.connect(
        user = conf.pg_user,
        password = conf.pg_pass,
        host = conf.pg_host,
        port = conf.pg_port,
        database = conf.pg_db
    )
    conn.autocommit = True
    return conn


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
                    status_code int not null,
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
                INSERT INTO website_metrics (url, response_time, status_code, regex_found)
                VALUES (%s, %s, %s, %s);
                """,
                (data.get('url'), data.get('response_time'), data.get('status_code'), data.get('regex_found'))
            )
    return
