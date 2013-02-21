import unittest
import datetime
import decimal
import json

from firebase.jsonutil import JSONEncoder


class JSONTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {'now': datetime.datetime.now(),
                     'oneday': datetime.timedelta(days=1),
                     'five': decimal.Decimal(5)}

    def test_conversion(self):
        serialized = json.dumps(self.data, cls=JSONEncoder)
        deserialized = json.loads(serialized)
        self.assertEqual(deserialized['oneday'],
                         int(self.data['oneday'].total_seconds()))
        self.assertTrue(type(deserialized['five']) == float)
        self.assertEqual(deserialized['five'], float(5))
        self.assertEqual(deserialized['now'], str(self.data['now'].isoformat()))

