import psycopg2
from threading import Timer

class RepeatedTimer(object):
    """Run python functions with a given interval 
    https://stackoverflow.com/a/38317060
    """
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False 


def init_postgres(config):
    """Initialize Postgres connection with parameters from the config object.

    Arguments:
        config (obj): Config object from the Postgres section of the config.ini file
    Returns:
        conn (obj): Postgres connection object
    """
    conn = psycopg2.connect(
        user = config['user'],
        password = config['password'],
        host = config['host'],
        port = config['port'],
        database = config['database']
    )
    conn.autocommit = True
    return conn