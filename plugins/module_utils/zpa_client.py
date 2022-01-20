# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c), Ansible Project 2017
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import re
from ansible.module_utils.common.text.converters import jsonify

__metaclass__ = type

import json
from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.pycompat24 import get_exception
import urllib.parse
import random
import time


def retry_with_backoff(retries=5, backoff_in_seconds=1):
    """
        This decorator should be used on functions that make HTTP calls and
        returns Response
    """
    def decorator(f):
        def wrapper(*args):
            x = 0
            while True:
                resp = f(*args)
                if resp.status_code < 299 or resp.status_code == 400:
                    return resp
                if x == retries:
                    raise Exception("Reached max retries: %s" % (resp.json))
                else:
                    sleep = (backoff_in_seconds * 2 ** x +
                             random.uniform(0, 1))
                    print("\n[INFO] args: %s\nretrying after %d seconds...\n" % (
                        str(args), sleep))
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator


def delete_none(f):
    """
        This decorator should be used on functions that return an object to delete empty fields
    """
    def wrapper(*args):
        _dict = f(*args)
        if _dict is not None:
            return deleteNone(_dict)
        return _dict
    return wrapper

def deleteNone(_dict):
    """Delete None values recursively from all of the dictionaries, tuples, lists, sets"""
    if isinstance(_dict, dict):
        for key, value in list(_dict.items()):
            if isinstance(value, (list, dict, tuple, set)):
                _dict[key] = deleteNone(value)
            elif value is None or key is None:
                del _dict[key]
    elif isinstance(_dict, (list, set, tuple)):
        _dict = type(_dict)(deleteNone(item)
                            for item in _dict if item is not None)
    return _dict


def camelcaseToSnakeCase(obj):
    new_obj = dict()
    for key, value in obj.items():
        if value is not None:
            new_obj[re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()] = value
    return new_obj

def snakecaseToCamelcase(obj):
    new_obj = dict()
    for key, value in obj.items():
        if value is not None:
            newKey = ''.join(
                x.capitalize() or '_' for x in key.split('_'))
            newKey = newKey[:1].lower() + newKey[1:]
            new_obj[newKey] = value
    return new_obj
class Response(object):
    def __init__(self, resp, info):
        self.body = None
        if resp:
            self.body = resp.read()
        self.info = info

    @property
    def json(self):
        if not self.body:
            if "body" in self.info:
                return json.loads(to_text(self.info.get("body")))
            return None
        try:
            return json.loads(to_text(self.body))
        except ValueError:
            return None

    @property
    def status_code(self):
        return self.info.get("status")


class ZPAClientHelper:
    def __init__(self, module):
        print("Hello there")
        self.baseurl = "https://config.private.zscaler.com"
        # self.private_baseurl = "https://api.private.zscaler.com"
        self.timeout = 240
        self.module = module
        self.client_id = module.params.get("client_id")
        self.client_secret = module.params.get("client_secret")
        self.customer_id = module.params.get("customer_id")
        self.tries = 0
        # login
        response = self.login()
        if response is None or response.status_code > 299 or response.json is None:
            self.module.fail_json(
                msg="Failed to login using provided credentials, please verify validity of API ZPA_CLIENT_ID & ZPA_CLIENT_SECRET. response: %s" % (
                    response)
            )
        resp_json = response.json
        self.access_token = resp_json.get("access_token")
        print("[INFO] access_token: '%s'" % (self.access_token))
        self.headers = {  # 'referer': self.baseurl,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': "Bearer %s" % (self.access_token)
        }

    @retry_with_backoff(retries=5)
    def login(self):
        """get jwt token"""
        data = urllib.parse.urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'application/json'}
        try:
            url = '%s/signin' % self.baseurl
            resp, info = fetch_url(
                module=self.module, url=url, data=data, method="POST", headers=headers)
            resp = Response(resp, info)
            print("[INFO] calling: %s %s %s\n response: %s" %
                  ("POST", url, str(data), str("" if resp == None else resp.json)))
            # print("[INFO] %s\n" % (to_text(resp.read())))
            return resp
        except Exception:
            e = get_exception()
            self._fail('login', str(e))

    def jsonify(self, data):
        try:
            return jsonify(data)
        except UnicodeError as e:
            self.fail_json(msg=to_text(e))

    def _fail(self, msg, e):
        if 'message' in e:
            err_string = e.get('message')
        else:
            err_string = e
        self.module.fail_json(msg='%s: %s' % (msg, err_string))

    def _url_builder(self, path):
        if path[0] == "/":
            path = path[1:]
        return "%s/%s" % (self.baseurl, path)

    @retry_with_backoff(retries=5)
    def send(self, method, path, data=None, fail_safe=False):
        url = self._url_builder(path)
        data = self.module.jsonify(data)
        if method == "DELETE":
            if data == "null":
                data = None

        resp, info = fetch_url(
            self.module,
            url,
            data=data,
            headers=self.headers,
            method=method,
            timeout=self.timeout,
        )
        resp = Response(resp, info)
        print("[INFO] calling: %s %s %s\n response: %s" %
              (method, url, str(data), str("" if resp == None else resp.json)))
        if resp.status_code == 400 and fail_safe == True:
            self.module.fail_json(
                msg="Operation failed. API response: %s\n" % (resp.json))
        return resp

    def get(self, path, data=None, fail_safe=False):
        return self.send("GET", path, data, fail_safe)

    def put(self, path, data=None):
        return self.send("PUT", path, data)

    def post(self, path, data=None):
        return self.send("POST", path, data)

    def delete(self, path, data=None):
        return self.send("DELETE", path, data)

    @staticmethod
    def zpa_argument_spec():
        return dict(
            client_id=dict(
                aliases=["client_id"],
                no_log=True,
                fallback=(
                    env_fallback,
                    ["ZPA_CLIENT_ID"],
                )
            ),
            client_secret=dict(
                aliases=["client_secret"],
                no_log=True,
                fallback=(
                    env_fallback,
                    ["ZPA_CLIENT_SECRET"],
                )
            ),
            customer_id=dict(
                aliases=["customer_id"],
                no_log=True,
                fallback=(
                    env_fallback,
                    ["ZPA_CUSTOMER_ID"],
                )
            )
        )

    def get_paginated_data(
        self,
        base_url=None,
        data_key_name=None,
        data_per_page=500,
        expected_status_code=200,
    ):
        """
        Function to get all paginated data from given URL
        Args:
            base_url: Base URL to get data from
            data_key_name: Name of data key value
            data_per_page: Number results per page (Default: 40)
            expected_status_code: Expected returned code from DigitalOcean (Default: 200)
        Returns: List of data

        """
        page = 0
        has_next = True
        ret_data = []
        status_code = None
        response = None
        while has_next or status_code != expected_status_code:
            required_url = "{0}?page={1}&pagesize={2}".format(
                base_url, page, data_per_page
            )
            response = self.get(required_url)
            status_code = response.status_code
            # stop if any error during pagination
            if status_code != expected_status_code:
                break
            page += 1
            if response is None or response.json is None or response.json.get(data_key_name) is None:
                has_next = False
                continue
            ret_data.extend(response.json[data_key_name])
            try:
                has_next = response.json.get("totalPages") is not None and int(
                    response.json["totalPages"]) != 0 and int(
                    response.json["totalPages"]) < page
            except KeyError:
                has_next = False

        if status_code != expected_status_code:
            msg = "Failed to fetch %s from %s" % (data_key_name, base_url)
            if response:
                msg += " due to error : %s" % response.json.get("message")
            self.module.fail_json(msg=msg)

        return ret_data
