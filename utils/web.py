import requests
import re


def collect_metrics(website, pattern=None):
    """Retrieve metrics (response time, status code) from a given website. 
    Optionally, search for a regex pattern. Then publish to a Kafka topic.

    Arguments:
        website (str): URL of website to collect metrics from
        pattern (str, optional): Regex pattern to look for
    Returns:
        data (dict): Key-value object with desired metrics
    """
    r = requests.get(website)

    # Try searching for regex pattern if provided
    match = None    
    if pattern and r.status_code == 200:
        match = True if re.search(pattern, r.text) else False

    data = {
        'url': website,
        'response_time': r.elapsed.total_seconds(),
        'status_code': r.status_code,
        'regex_found': match
    }

    return data