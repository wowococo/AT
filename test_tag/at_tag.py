# coding=utf8

import json
import yaml
import requests
import pytest


REQUEST_RESOURCE = ['tag', 'group', 'link']
POST

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
    resource = extract_conf(resource).get('POST')
    if resource:
        url = resource['url']
        body = resource['body']
        for case in body.keys():
            data = json.dumps(body[case])
            res = send_request('POST', url, data)
            yield res

def send_put(resource):
    resource = extract_conf(resource).get('PUT')

def combine(resource, method):
    # res = send_post(resource)
    res = eval(f"send_{method.lower()}")
    expected_res = extract_conf(resource).get(method).get('expected_res')
    return zip(res, expected_res)


@pytest.mark.parametrize("a, expected", 
                         (lambda resource, method: combine(resource, method))('link', 'POST'))
def test_send_post_link(a, expected):
    start_assert(a, expected)
    # assert a.status_code == expected[0]
    # text = json.loads(a.text)
    # if "code" in text:
    #     assert text['code'] == expected[1]
    # if 'message' in text:
    #     assert text['message'] == expected[2]


@pytest.mark.parametrize("a, expected", 
                         (lambda resource, method: combine(resource, method))('tag', 'POST'))
def test_send_post_tag(a, expected):
    start_assert(a, expected)
    # assert a.status_code == expected[0]
    # text = json.loads(a.text)
    # if "code" in text:
    #     assert text['code'] == expected[1]
    # if 'message' in text:
    #     assert text['message'] == expected[2]

@pytest.mark.parametrize("a, expected", 
                         (lambda resource, method: combine(resource, method))('tag', 'PUT'))
def test_put_post_tag(a, expected):
    start_assert(a, expected)


def start_assert(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]


