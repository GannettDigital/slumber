import time
import slumber
import unittest
import json
import datetime


def default(obj):
    if type(obj) is datetime.datetime:
        return {"epoch-ms": time.mktime(obj.timetuple())}
    else:
        return obj


def object_hook(obj):
    if "epoch-ms" in obj:
        return datetime.datetime.fromtimestamp(obj["epoch-ms"])
    else:
        return obj


def custom_loads(*args, **kwargs):
    kwargs['object_hook'] = object_hook
    return json.loads(*args, **kwargs)


def custom_dumps(*args, **kwargs):
    # warning, this clobbers an existing default,
    # in create a composition function that returns
    # kwargs['default'](default(obj))
    kwargs['default'] = default
    return json.dumps(*args, **kwargs)


class CustomCodecs(unittest.TestCase):

    def test(self):
        expected = datetime.datetime.fromtimestamp(1333734819.0)

        api = slumber.API("http://www.example.com/v1",
                          custom_codecs={"json": (custom_dumps, custom_loads)})

        resource = api.resource
        serializer = resource.get_serializer()
        
        result = serializer.loads("""{"epoch-ms": 1333734819.0}""")
        self.assertEqual(result, expected)

        result = serializer.dumps(expected)
        self.assertEqual(result, """{"epoch-ms": 1333734819.0}""")

    
