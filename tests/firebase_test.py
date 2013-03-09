import unittest
import os
import requests
import json

from firebase.firebase import (FirebaseAuthentication, FirebaseApplication,
                               make_get_request, make_post_request, make_put_request,
                               make_patch_request, make_delete_request)


class MockConnection(object):
    def __init__(self, response):
        self.response = response
        self.headers = {}

    def get(self, url, params, headers, *args, **kwargs):
        return self.response

    def post(self, url, data, params, headers, *args, **kwargs):
        return self.response

    def put(self, url, data, params, headers, *args, **kwargs):
        return self.response

    def patch(self, url, data, params, headers, *args, **kwargs):
        return self.response

    def delete(self, url, params, headers, *args, **kwargs):
        return self.response


class MockResponse(object):
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    @property
    def ok(self):
        return str(self.status_code).startswith('2')

    def json(self):
        if self.content:
            return json.loads(self.content)
        return None

    def raise_for_status(self):
        raise Exception('Fake HTTP Error')


class FirebaseTestCase(unittest.TestCase):
    def setUp(self):
        self.SECRET = 'FAKE_FIREBASE_SECRET'
        self.DSN = 'https://firebase.localhost'
        self.EMAIL = 'python-firebase@firebase.com'
        self.authentication = FirebaseAuthentication(self.SECRET, self.EMAIL,
                                                     None)
        self.firebase = FirebaseApplication(self.DSN, self.authentication)

    def test_build_endpoint_url(self):
        url1 = os.path.join(self.DSN, 'users', '1.json')
        self.assertEqual(self.firebase._build_endpoint_url('/users', '1'), url1)
        url2 = os.path.join(self.DSN, 'users/1/.json')
        self.assertEqual(self.firebase._build_endpoint_url('/users/1', None), url2)

    def test_make_get_request(self):
        response = MockResponse(403, json.dumps({'error': 'Permission required.'}))
        connection = MockConnection(response)
        result = self.firebase.get('url', 'shapshot', params={}, headers={},
                                   connection=connection)
        self.assertEqual(result, json.loads(response.content))

    def test_make_post_request(self):
        response = MockResponse(403, json.dumps({'error': 'Permission required.'}))
        connection = MockConnection(response)
        result = self.firebase.post('url', {}, params={}, headers={},
                                    connection=connection)
        self.assertEqual(result, json.loads(response.content))

    def test_make_put_request(self):
        response = MockResponse(403, json.dumps({'error': 'Permission required.'}))
        connection = MockConnection(response)
        result = self.firebase.put('url', 'snapshot', {}, params={}, headers={},
                                   connection=connection)
        self.assertEqual(result, json.loads(response.content))

    def test_make_patch_request(self):
        response = MockResponse(403, json.dumps({'error': 'Permission required.'}))
        connection = MockConnection(response)
        result = self.firebase.patch('url', {}, params={}, headers={},
                                     connection=connection)
        self.assertEqual(result, json.loads(response.content))

    def test_make_delete_request(self):
        response = MockResponse(403, json.dumps({'error': 'Permission required.'}))
        connection = MockConnection(response)
        result = self.firebase.delete('url', 'snapshot', params={}, headers={},
                                      connection=connection)
        self.assertEqual(result, json.loads(response.content))
