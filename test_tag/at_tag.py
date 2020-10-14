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

def send_post_link():
    link = extract_conf('link')
    link_url = link['url']
    body_key, body_values = link['body_key'], link['body_value']
    for v in body_values:
        data = json.dumps(dict(zip(body_key, v)))
        # print(data)
        res = send_request('POST', link_url, data)
        yield res

def combine():
    res = send_post_link()
    expected_res = extract_conf('link')['response']
    return zip(res, expected_res)


@pytest.mark.parametrize("a, expected", combine())
def test_send_post_link(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]


        



