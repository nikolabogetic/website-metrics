from utils.web import collect_metrics

def test_collect_metrics_200():
    r = collect_metrics('https://httpstat.us/200')
    assert r.get('url') == 'https://httpstat.us/200'
    assert r.get('status_code') == 200
    assert r.get('response_time') > 0
    assert r.get('regex_found') == None

def test_collect_metrics_500():
    r = collect_metrics('https://httpstat.us/500')
    assert r.get('url') == 'https://httpstat.us/500'
    assert r.get('status_code') == 500
    assert r.get('response_time') > 0
    assert r.get('regex_found') == None

def test_collect_metrics_wiki_good_regex():
    r = collect_metrics('https://www.wikipedia.org/', pattern="English")
    assert r.get('url') == 'https://www.wikipedia.org/'
    assert r.get('status_code') == 200
    assert r.get('response_time') > 0
    assert r.get('regex_found') == True

def test_collect_metrics_wiki_bad_regex():
    r = collect_metrics('https://www.wikipedia.org/', pattern="OIWQWFHBVWFJODSDF")
    assert r.get('url') == 'https://www.wikipedia.org/'
    assert r.get('status_code') == 200
    assert r.get('response_time') > 0
    assert r.get('regex_found') == False