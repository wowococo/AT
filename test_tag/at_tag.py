# coding=utf8

import yaml
import requests
import pytest


REQUEST_RESOURCE = ['tag', 'group', 'link']


class TestTag():

    def send_request(self, method, url, data=None):
        if method == "POST":
            r = requests.post(url, data)
        elif method == "PUT":
            r = requests.put(url, data)
        elif method == "GET":
            r = requests.get(url)
        else:
            r = requests.delete(url)

        return r

    def load_config(self):
        with open('conf.yml', 'r') as f:
            return yaml.load(f.read())

    def extract_conf(self, resource):
        conf = self.load_config()
        if resource == 'link':
            return conf['link']

    def send_post_link(self):
        link = self.extract_conf('link')
        link_url = link['url'],
        body_key, body_values = link['body_key'], link['body_value']
        for v in body_values:
            data = dict(zip(body_key, v))
            res = self.send_request('POST', link_url, data)
            yield res

    def test_post_link(self, expected_res):
        res = self.send_post_link()
        for r, expected_r in zip(res, expected_res):
            print(r, r.text)
            assert(r.status_code == expected_r[0])
            assert(r.text)




        




