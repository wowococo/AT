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
    with open('conf.yml', 'r') as f:
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
    resource = extract_conf(resource)['post']
    resource_url = link['url']
    body_key, body_values = resource['body_key'], resource['body_value']
    for v in body_values:
        data = json.dumps(dict(zip(body_key, v)))
        # print(data)
        res = send_request('POST', link_url, data)
        yield res

def combine(resource, method):
    res = send_post(resource)
    expected_res = extract_conf(resource)[method]['response']
    return zip(res, expected_res)


@pytest.mark.parametrize("a, expected", combine())
def test_send_post(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]


def test_send_post_tag():



        



