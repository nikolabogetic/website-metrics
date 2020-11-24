# website-metrics

![Python application](https://github.com/nikolabogetic/website-metrics/workflows/Python%20application/badge.svg)

This repository contains the following utilities:

`website_checker` is used to collect metrics from a given website and send them to a Kafka broker. 

`database_writer` is used to receive messages from a Kafka broker and write them to a Postgres database.

Requires Python 3.6 or newer.

## Setup

### Initial setup
```
$ python3 init_config.py
```
The `init_config.py` script helps create a `.env` configuration file. It will interactively prompt you for connection parameters, as well as instruct you to place the Kafka certificate files in `certs/`.

Example `.env` file:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=postgres

KAFKA_URI=localhost:9092
KAFKA_TOPIC=website-metrics

WEBSITE_URL=https://example.org/
TIME_INTERVAL=3
REGEX_PATTERN="Domain"
```

## Usage

### Option 1: Running manually in a local virtual environment
Once `.env` is configured and the certificate files are in place, run the following commands to set up the virtual environment:
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
To start the database writer:
```
$ python database_writer.py
```
To start the website checker:
```
$ python website_checker.py
```

### Option 2: Running with Docker
Once `.env` is configured and the certificate files are in place, you can run the whole package with docker-compose:
```
$ docker-compose build
$ docker-compose up
```
This will run both utilities in separate containers.

You can always set the parameters directly in `docker-compose.yml` if you prefer, or override them on the command line, like so:
```
$ WEBSITE_URL=https://wikipedia.org/ REGEX_PATTERN="English" docker-compose up
```

## Testing

GitHub Actions workflow is used to build and test the application automatically.

### Running pytest manually in virtual environment
For tests, it is assumed that connection parameters and Kafka certificate files are configured (either using `init_config.py`, or manually).

```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pytest -v --cov
```

