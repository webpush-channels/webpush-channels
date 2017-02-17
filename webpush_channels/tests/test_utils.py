from collections import OrderedDict
from webpush_channels.utils import canonical_json


def test_canonical_json_sorts_keys():
    d1 = OrderedDict()
    d1['foobar'] = 2
    d1['dodo'] = 1
    d2 = OrderedDict()
    d2['dodo'] = 1
    d2['foobar'] = 2

    assert canonical_json(d1) == canonical_json(d2)
