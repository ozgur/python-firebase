# Python Firebase

The python interface to the Firebase's REST API.

## Installation

    $ git clone git@github.com:ozgur/python-firebase.git
    $ python setup.py install

## Getting Started

You can fetch any of your data in JSON format by appending '.json' to the end of the URL in which your data resides and, then send an HTTPS request through your browser. Like all other REST specific APIs, Firebase offers a client to update(PATCH, PUT), create(POST), or remove(DELETE) his stored data along with just to fetch it.

To fetch all the users in your storage simply do the following:


The second argument of **get** method is the name of the snapshot. Thus, if you leave it NULL you get the data in the URL **/users.json**. Besides, if you set it to **1**, you get the data in the url */users/1.json*. In other words, you get the user whose ID equals to 1.

    >>> result = firebase.get('/users', '1')
    >>> print result
    >>> {'1': 'John Doe'}


```python
from firebase import firebase
firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
result = firebase.get('/users', None)
print result
{'1': 'John Doe', '2': 'Jane Doe'}
```

The library provides all the correspoding methods for those actions in both synchoronous and asynchronous manner. You can just start an asynchronous GET request with your callback function, and the method
