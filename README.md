# website-metrics

This repository contains the following utilities:

`website_checker.py` is used to collect metrics from a given website and send them to a Kafka broker. 

`database_writer.py` is used to receive messages from a Kafka broker and write them to a Postgres database.

Requires Python 3.6 or newer.

## Setup

Installing in virtualenv:
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install requirements.txt
$ python3 init_config.py
```
Running the `init_config.py` script will interactively prompt you for Kafka and Postgres connection information, as well as instruct you where to place the certificate files.


## Usage

### website_checker:
```
$ python3 website_checker.py -t <time_interval> --url <website_to_scrape> \
    [--pattern <regex_patern>]
```

Here's an example that will make requests to Wikipedia every 5 seconds and look for the word "English":

```
$ python3 website_checker.py -t 5 --url https://www.wikipedia.org/ --pattern "English"
```
Another example without Regex:
```
$ python3 website_checker.py -t 5 --url https://www.example.org/
```

### database_writer:
```
$ python3 database_writer.py 
```


## Testing
For tests, it is assumed that Kafka certificates, as well as Kafka and Postgres connection parameters, are configured using `init_config.py`.

```
$ pip install pytest
$ pytest
```
