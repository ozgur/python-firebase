# Python Firebase

The python interface to the Firebase's REST API.

## Installation

    $ git clone git@github.com:ozgur/python-firebase.git
    $ python setup.py install

## Getting Started

You can fetch any of your data in JSON format by appending '.json' to the end of the URL in which your data resides and, then send an HTTPS request through your browser. Like all other REST specific APIs, Firebase offers a client to update(PATCH, PUT), create(POST), or remove(DELETE) his stored data along with just to fetch it.

To fetch all the users in your storage simply do the following:

```python
from firebase import firebase
firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
result = firebase.get('/users', None)
print result
{'1': 'John Doe', '2': 'Jane Doe'}
```


The second argument of **get** method is the name of the snapshot. Thus, if you leave it NULL, you get the data in the URL **/users.json**. Besides, if you set it to **1**, you get the data in the url **/users/1.json**. In other words, you get the user whose ID equals to 1.

```python
from firebase import firebase
firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
result = firebase.get('/users', '1')
print result
{'1': 'John Doe'}
```

You can also provide extra query parameters that will be appended to the url or extra key-value pairs sent in the HTTP header.

```python
from firebase import firebase
firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
result = firebase.get('/users/2', None, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print result
{'2': 'Jane Doe'}
```

Creating new data requires a POST or PUT request. Assuming you didn't append **print=silent** to the url, if you use POST the returning value becomes the name of the snapshot, if PUT you get the data you just sent. If print=silent is provided, you get just NULL because the backend does not send any output.

```python
from firebase import firebase
firebase = firebase.FirebaseApplication('https://your_storage.firebaseio.com', None)
new_user = 'Ozgur Vatansever'
result = firebase.post('/users', new_user, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print result
{'name'': 'Jane Doe'}

result = firebase.post('/users', new_user, {'print': 'silent'}, {'X_FANCY_HEADER': 'VERY FANCY'})
print result == None
True
```



The library provides all the correspoding methods for those actions in both synchoronous and asynchronous manner. You can just start an asynchronous GET request with your callback function, and the method
