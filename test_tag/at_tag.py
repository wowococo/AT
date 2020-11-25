# coding=utf8

import json
import yaml
import requests
import pytest
from collections import namedtuple

Resource = namedtuple('Resource', ['tag', 'link', 'group', 'tree', 'ftopt'])
src = Resource('tag', 'link', 'group', 'tree', 'ftopt')
POST, PUT, GET, DELETE = 'POST', 'PUT', 'GET', 'DELETE'


def send_request(method, url, data=None):
    if method == POST:
        r = requests.post(url, data)
    elif method == PUT:
        r = requests.put(url, data)
    elif method == GET:
        r = requests.get(url)
    else:
        r = requests.delete(url)

    return r


def load_config():
    with open('conf.yml', 'rb') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)


def extract_conf(resource):
    config = load_config()
    if resource == src.group:
        return config[src.group]
    elif resource == src.tag:
        return config[src.tag]
    else:
        return config[src.link]


def send_post(resource):
    conf = extract_conf(resource).get(POST)
    if conf:
        url = conf['url']
        body = conf['body']
        for case in body.keys():
            data = json.dumps(body[case])
            res = send_request(POST, url, data)
            yield res


def send_put(resource):
    conf = extract_conf(resource).get(PUT)
    if conf:
        urls = conf['url']
        body = conf['body']
        for tc in urls:
            url = urls[tc]
            datas = body[tc]
            for case in datas.keys():
                data = json.dumps(datas[case])
                res = send_request(PUT, url, data)
                yield res


def send_delete(resource):
    conf = extract_conf(resource).get(DELETE)
    if conf:
        urls = conf.get('url')
        for case in urls.keys():
            res = send_request(DELETE, url=urls[case])
            yield res


def send_get(resource):
    conf = extract_conf(resource).get(GET)
    if conf:
        urls = conf.get('url')
        for case in urls.keys():
            res = send_request(GET, url=urls[case])
            yield res


def combine(resource, method):
    str = f"send_{method.lower()}('{resource}')"
    res = eval(str)
    expected_res = extract_conf(resource).get(method).get('expected_res')
    expected_res = expected_res.values()
    return zip(res, expected_res)


def start_assert(a, expected):
    assert a.status_code == expected[0]
    text = json.loads(a.text)
    if "code" in text:
        assert text['code'] == expected[1]
    if 'message' in text:
        assert text['message'] == expected[2]


# -----------------------------------------------------
# test link
# ----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.link, POST))
def test_send_post_link(a, expected):
    start_assert(a, expected)


# @pytest.mark.parametrize("a, expected", (
#     lambda resource, method: combine(resource, method))(src.link, PUT))
# def test_send_put_link(a, expected):
#     start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.link, DELETE))
def test_send_delete_link(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.link, GET))
def test_send_get_link(a, expected):
    start_assert(a, expected)


# -----------------------------------------------------
# test tag
# -----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.tag, POST))
def test_send_post_tag(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.tag, PUT))
def test_send_put_tag(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.tag, DELETE))
def test_send_delete_tag(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.tag, GET))
def test_send_get_tag(a, expected):
    start_assert(a, expected)


# -----------------------------------------------------
# test taggroup
# -----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.group, POST))
def test_send_post_group(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.group, PUT))
def test_send_put_group(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.group, DELETE))
def test_send_delete_group(a, expected):
    start_assert(a, expected)


@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.group, GET))
def test_send_get_group(a, expected):
    start_assert(a, expected)


# -----------------------------------------------------
# test tagtree
# -----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.tree, GET))
def test_send_get_tree(a, expected):
    start_assert(a, expected)


# -----------------------------------------------------
# test tag-filter-options
# -----------------------------------------------------
@pytest.mark.parametrize("a, expected", (
    lambda resource, method: combine(resource, method))(src.ftopt, GET))
def test_send_get_filter_options(a, expected):
    start_assert(a, expected)
