Python Firebase
=================

Python interface to Firebase's REST API

.. image:: https://travis-ci.org/ozgur/python-firebase.png?branch=master
   :target: https://travis-ci.org/ozgur/python-firebase

Installation
-----------------

python-firebase depends heavily on the **requests** library.

.. code-block:: bash

    $ sudo pip install requests==1.1.0
    $ sudo pip install python-firebase

Getting Started
------------------

You can read or write any of your data in JSON format. Append '.json' to the end of the URL in which your data resides. Send an HTTPS request from the browser. You can read (GET), replace (PUT), selectively update (PATCH), append (POST), or remove (DELETE) data From firebase.

The library provides all the correspoding methods for those actions in both synchoronous and asynchronous manner. 

To read some data, start an asynchronous GET request with your callback function. For example, to fetch the entire content of "/users" in your Firebase database called "your_storage", do the following:

.. code-block:: python

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
    result = firebase.get('/users', None)
    print result
    {'1': 'John Doe', '2': 'Jane Doe'}

The second argument of **get** method is the branch of the database you wish to read. If you leave it None, you get all the data in the URL **/users.json**. If, instead, you set it to **1**, you get the data in the url **/users/1.json**. In other words, you get the user whose ID equals to 1.

.. code-block:: python

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
    result = firebase.get('/users', '1')
    print result
    {'1': 'John Doe'}

You can also provide extra query parameters that will be appended to the url or extra key-value pairs sent in the HTTP header.

.. code-block:: python

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
    result = firebase.get('/users/2', None, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
    print result
    {'2': 'Jane Doe'}

Creating new data requires a PUT or POST request. If you know exactly where you want to put the data, use PUT. If you just want to append some data under a new key, but don't want to tell Firebase what key to use, use POST and Firebase will create a unique time-ordered key. 

By default, in POST the function returns the a dictionary containing in "name", the key it has created for the data you have written, and in PUT the function returns the data you have just sent. If, instead, you set print=silent, the function returns None because the backend never sends an output.

.. code-block:: python

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
    new_user = 'Ozgur Vatansever'

    result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
    print result
    {u'name': u'-Io26123nDHkfybDIGl7'}

    result = firebase.post('/users', new_user, {'print': 'silent'}, {'X_FANCY_HEADER': 'VERY FANCY'})
    print result == None
    True

Deleting data is relatively easy compared to other actions. You just specify the url. The backend sends no output.

.. code-block:: python

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
    firebase.delete('/users', '1')
    # John Doe goes away.

Authentication
------------------

Authentication in Firebase involves simply creating a token that conforms to the JWT standarts and putting it into the querystring with the name **auth**. The library creates that token for you so you never end up struggling with constructing a valid token on your own. If the data has been protected against write/read operations with some security rules, the backend sends an appropriate error message back to the client with the status code **403 Forbidden**.

.. code-block:: python

    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', authentication=None)
    result = firebase.get('/users', None, {'print': 'pretty'})
    print result
    {'error': 'Permission denied.'}

    authentication = firebase.FirebaseAuthentication('THIS_IS_MY_SECRET', 'ozgurvt@gmail.com', extra={'id': 123})
    firebase.authentication = authentication
    print authentication.extra
    {'admin': False, 'debug': False, 'email': 'ozgurvt@gmail.com', 'id': 123, 'provider': 'password'}

    user = authentication.get_user()
    print user.firebase_auth_token
    "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhZG1pbiI6IGZhbHNlLCAiZGVidWciOiBmYWxzZSwgIml
    hdCI6IDEzNjE5NTAxNzQsICJkIjogeyJkZWJ1ZyI6IGZhbHNlLCAiYWRtaW4iOiBmYWxzZSwgInByb3ZpZGVyIjog
    InBhc3N3b3JkIiwgImlkIjogNSwgImVtYWlsIjogIm96Z3VydnRAZ21haWwuY29tIn0sICJ2IjogMH0.lq4IRVfvE
    GQklslOlS4uIBLSSJj88YNrloWXvisRgfQ"

    result = firebase.get('/users', None, {'print': 'pretty'})
    print result
    {'1': 'John Doe', '2': 'Jane Doe'}


Concurrency
------------------

The interface heavily depends on the standart **multiprocessing** library when concurrency comes in. While creating an asynchronous call, an on-demand process pool is created and, the async method is executed by one of the idle process inside the pool. The pool remains alive until the main process dies. So every time you trigger an async call, you always use the same pool. When the method returns, the pool process ships the returning value back to the main process within the callback function provided.

.. code-block:: python

    import json
    from firebase import firebase
    from firebase import jsonutil

    firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', authentication=None)

    def log_user(response):
        with open('/tmp/users/%s.json' % response.keys()[0], 'w') as users_file:
            users_file.write(json.dumps(response, cls=jsonutil.JSONEncoder))

    firebase.get_async('/users', None, {'print': 'pretty'}, callback=log_user)


TODO
---------

* Async calls must deliver exceptions raised back to the main process.
* More regression/stress tests on asynchronous calls.
* Docs must be generated.
