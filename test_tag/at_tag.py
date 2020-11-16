# coding=utf8

import json
import yaml
import requests
import pytest


REQUEST_RESOURCE = ['tag', 'group', 'link']


# class TestTag():

def send_request(method, url, data=None):
    if method == "POST":
        r = requests.post(url, data)
    elif method == "PUT":
        r = requests.put(url, data)
    elif method == "GET":
        r = requests.get(url)
    else:
        r = requests.delete(url)

    return r

def load_config():
    with open('conf.yml', 'rb') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)

def extract_conf(resource):
    conf = load_config()
    if resource == 'link':
        return conf['link']
    elif resource == 'tag':
        return conf['tag']
    else:
        return conf['link']

def send_post(resource):
    resource = extract_conf(resource)['POST']
    url = resource['url']
    body = resource['body']
    # keys, values = body['legal_keys'], body['values']
    
    for testcase in range(len(body.keys())):
        data = json.dumps(testcase)
        res = send_request('POST', url, data)
        yield res

def combine(resource, method):
    res = send_post(resource)
    expected_res = extract_conf(resource)[method]['expected_res']
    return zip(res, expected_res)


@pytest.mark.parametrize("a, expected", 
                         (lambda resource, method: combine(resource, method))('link', 'POST'))
def test_send_post_link(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]


@pytest.mark.parametrize("a, expected", 
                         (lambda resource, method: combine(resource, method))('tag', 'POST'))
def test_send_post_tag(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]
    



