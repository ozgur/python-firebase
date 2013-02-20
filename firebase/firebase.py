import urlparse
import json

from firebase_token_generator import FirebaseTokenGenerator
from decorators import http_connection

from async import process_pool


@http_connection(60)
def make_get_request(url, params, headers, connection):
    return json.loads(connection.get(url, params=params, headers=headers).content)


@http_connection(30)
def make_put_request(url, params, data, headers, connection):
    response = connection.put(url, data=data, params=params, headers=headers)
    response.raise_for_status()
    return True


@http_connection(30)
def make_post_request(url, params, data, headers, connection):
    response = connection.post(url, params=params, data=data, headers=headers)
    response.raise_for_status()
    return json.loads(response.content)


@http_connection(60)
def make_patch_request(url, params, data, headers, connection):
    response = connection.patch(url, params=params, data=data, headers=headers)
    response.raise_for_status()
    return json.loads(response.content)


@http_connection(30)
def make_delete_request(url, params, headers, connection):
    response = connection.delete(url, params=params, headers=headers)
    response.raise_for_status()
    return True


class FirebaseUser(object):
    """
    Class that wraps the credentials of the authenticated user.
    """
    def __init__(self, email, firebase_auth_token, provider, id=None):
        self.email = email
        self.firebase_auth_token = firebase_auth_token
        self.provider = provider
        self.id = id


class FirebaseAuthentication(object):
    """
    Class that wraps the Firebase SimpleLogin mechanism. Actually this
    class does not trigger a connection, simply fakes the auth action.

    In addition, the provided email and password information is totally
    useless and they never appear in the ``auth`` variable at the server.
    """
    def __init__(self, secret, email, password):
        self.authenticator = FirebaseTokenGenerator(secret)
        self.email = email
        self.password = password
        self.provider = 'password'

    def get_user(self, extra_data=None):
        """
        Method that gets the authenticated user. The returning user has
        the token, email and the provider data.
        """
        if not extra_data:
            extra_data = {}
        extra_data.update({'email': self.email, 'provider': self.provider})
        token = self.authenticator.create_token(extra_data)
        return FirebaseUser(self.email, token, self.provider)


class FirebaseApplication(object):
    NAME_EXTENSION = '.json'
    URL_SEPERATOR = '/'

    def __init__(self, dsn, authentication=None):
        assert dsn.startswith('https://'), 'DSN must be a secure URL'
        self.dsn = dsn
        self.authentication = authentication

    def _build_endpoint_url(self, url, name=None):
        if not url.endswith(self.URL_SEPERATOR):
            url = url + self.URL_SEPERATOR
        if name is None:
            name = ''
        return '%s%s%s' % (urlparse.urljoin(self.dsn, url), name,
                           self.NAME_EXTENSION)

    def _authenticate(self, params, headers):
        if self.authentication:
            headers.update(self.authentication.authenticator.HEADERS)
            user = self.authentication.get_user()
            params.update({'auth': user.firebase_auth_token})

    @http_connection(60)
    def get(self, url, name, connection, params={}, headers={}):
        """
        Synchronous GET request.
        """
        if name is None: name = ''
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        response = connection.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return json.loads(response.content)

    def get_async(self, url, name, callback=None, params={}, headers={}):
        """
        Asynchronous GET request with the process pool.
        """
        if name is None: name = ''
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        process_pool.apply_async(make_get_request,
            args=(endpoint, params, headers), callback=callback)

    @http_connection(30)
    def put(self, url, name, data, connection, params={}, headers={}):
        """
        Synchronous PUT request. There will be no returning output from
        the server, because the request will be made with ``silent``
        parameter. ``data`` must be a JSONable value.
        """
        assert name, 'Snapshot name must be specified'
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        params.update({'print': 'silent'})
        response = connection.put(endpoint, data=json.dumps(data),
                                  params=params, headers=headers)
        response.raise_for_status()
        return True

    def put_async(self, url, name, data, params={}, headers={}):
        """
        Asynchronous PUT request with the process pool.
        """
        if name is None: name = ''
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        params.update({'print': 'silent'})
        data = json.dumps(data)
        process_pool.apply_async(make_put_request,
                                 args=(endpoint, params, data, headers),
                                 callback=None)

    @http_connection(30)
    def post(self, url, data, connection, params={}, headers={}):
        """
        Synchronous POST request. ``data`` must be a JSONable value.
        """
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        params.pop('print', None)
        response = connection.post(endpoint, data=json.dumps(data),
                                   params=params, headers=headers)
        response.raise_for_status()
        return json.loads(response.content)

    def post_async(self, url, data, callback=None, params={}, headers={}):
        """
        Asynchronous POST request with the process pool.
        """
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        params.pop('print', None)
        data = json.dumps(data)
        process_pool.apply_async(make_post_request,
                                 args=(endpoint, params, data, headers),
                                 callback=callback)

    @http_connection(60)
    def patch(self, url, data, connection, params={}, headers={}):
        """
        Synchronous POST request. ``data`` must be a JSONable value.
        """
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        params.pop('print', None)
        response = connection.patch(endpoint, data=json.dumps(data),
                                    params=params, headers=headers)
        response.raise_for_status()
        return json.loads(response.content)

    def patch_async(self, url, data, callback=None, params={}, headers={}):
        """
        Asynchronous PATCH request with the process pool.
        """
        endpoint = self._build_endpoint_url(url, None)
        self._authenticate(params, headers)
        params.pop('print', None)
        data = json.dumps(data)
        process_pool.apply_async(make_patch_request,
                                 args=(endpoint, params, data, headers),
                                 callback=callback)

    @http_connection(30)
    def delete(self, url, name, connection, params={}, headers={}):
        """
        Synchronous DELETE request. ``data`` must be a JSONable value.
        """
        if not name: name = ''
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        params.update({'print': 'silent'})
        response = connection.delete(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return True

    def delete_async(self, url, name, callback=None, params={}, headers={}):
        """
        Asynchronous DELETE request with the process pool.
        """
        if not name: name = ''
        endpoint = self._build_endpoint_url(url, name)
        self._authenticate(params, headers)
        params.update({'print': 'silent'})
        print endpoint, params, headers
        process_pool.apply_async(make_delete_request,
                    args=(endpoint, params, headers), callback=callback)

