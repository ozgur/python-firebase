import urlparse
import requests
import json

from firebase_token_generator import FirebaseTokenGenerator
from decorators import http_connection

from async import process_pool


@http_connection(60)
def make_get_request(url, params, headers, connection):
    return connection.get(url, params=params, headers=headers).content


def response_to_json(response):
    return json.loads(response)


class FirebaseUser(object):
    """
    Class that wraps the credentials of authenticated user.
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

    @http_connection(60)
    def get(self, url, name, connection, params={}, headers={}):
        """
        Synchronous GET request.
        """
        if name is None: name = ''
        endpoint = self._build_endpoint_url(url, name)
        if self.authentication:
            headers.update(self.authentication.authenticator.HEADERS)
            user = self.authentication.get_user()
            params.update({'auth': user.firebase_auth_token})
        response = connection.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response_to_json(response.content)

    def get_async(self, url, name, params={}, headers={}):
        """
        Asynchronous GET request with the process pool.
        """
        endpoint = self._build_endpoint_url(url, name)
        if self.authentication:
            user = self.authentication.get_user()
            params.update({'auth': user.firebase_auth_token})
        headers.update(self.authentication.authenticator.HEADERS)
        process_pool.apply_async(make_get_request, args=(endpoint, params, headers),
                                 callback=response_to_json)
