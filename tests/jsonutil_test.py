import unittest
import datetime
import decimal
import json

from firebase.jsonutil import JSONEncoder


class JSONTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {'now': datetime.datetime.now(),
                     'oneday': datetime.timedelta(days=1),
                     'five': decimal.Decimal(5),
                     'date': datetime.date(2014, 3, 11)}

    def test_conversion(self):
        serialized = json.dumps(self.data, cls=JSONEncoder)
        deserialized = json.loads(serialized)
        self.assertEqual(deserialized['oneday'], 86400)
        self.assertTrue(type(deserialized['five']) == float)
        self.assertEqual(deserialized['five'], float(5))
        self.assertEqual(deserialized['now'], str(self.data['now'].isoformat()))
        self.assertEqual(deserialized['date'], str(self.data['date'].isoformat()))

    def test_total_seconds(self):
        from firebase.jsonutil import total_seconds

        delta = datetime.timedelta(days=1,
                                   seconds=3,
                                   microseconds=440000,
                                   milliseconds=3300,
                                   minutes=5,
                                   hours=2,
                                   weeks=2)

        self.assertEqual(total_seconds(delta), 1303506.74)

