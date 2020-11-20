# coding=utf8

import json
import yaml
import requests
import pytest
from collections import namedtuple

Resource = namedtuple('Resource', ['tag', 'link', 'group'])
src = Resource('tag', 'link', 'group')
METHOD = {"post": "POST", "put": "PUT", "get": "GET", "delete": "DELETE"}


def send_request(method, url, data=None):
    if method == METHOD['post']:
        r = requests.post(url, data)
    elif method == METHOD['put']:
        r = requests.put(url, data)
    elif method == METHOD['get']:
        r = requests.get(url)
    else:
        r = requests.delete(url)

    return r


def load_config():
    with open('conf.yml', 'rb') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def extract_conf(resource):
    conf = load_config()
    if resource == src.group:
        return conf[src.group]
    elif resource == src.tag:
        return conf[src.tag]
    else:
        return conf[src.link]


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
    if resource:
        urls = resource('url')
        body = resource('body')
        for tc in urls:
            url = urls[tc]
            body = body['tc']
            for case in body.keys():
                data = json.dumps(body[case])
                res = send_request('PUT', url, data)
                yield res


def send_delete(resource):
    resource = extract_conf(resource).get('DELETE')
    if resource:
        urls = resource('url')
        for case in urls.keys():
            res = send_request('DELETE', url=urls[case])
            yield res


def send_get(resource):
    pass


def combine(resource, method):
    str = f"send_{method.lower()}({resource})"
    print('ee', str)
    res = eval(str)
    # res = eval('send_post(resource)')
    expected_res = extract_conf(resource).get(method).get('expected_res')
    expected_res = expected_res.values()
    return zip(res, expected_res)


# -----------------------------------------------------
# test link
# ----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('link', 'POST'))
def test_send_post_link(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('link', 'PUT'))
def test_send_put_link(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('link', 'DELETE'))
def test_send_delete_link(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('link', 'GET'))
def test_send_get_link(a, expected):
    start_assert(a, expected)


# -----------------------------------------------------
# test tag
# -----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('tag', 'POST'))
def test_send_post_tag(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('tag', 'PUT'))
def test_send_put_tag(a, expected):
    start_assert(a, expected)

@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('tag', 'DELETE'))
def test_send_delete_tag(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('tag', 'GET'))
def test_send_get_tag(a, expected):
    start_assert(a, expected)


# -----------------------------------------------------
# test taggroup
# -----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('group', 'POST'))
def test_send_post_group(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('group', 'PUT'))
def test_send_put_group(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('group', 'DELETE'))
def test_send_delete_group(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))('group', 'GET'))
def test_send_get_group(a, expected):
    start_assert(a, expected)


def start_assert(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]
