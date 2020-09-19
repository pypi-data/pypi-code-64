import sys

if sys.version_info > (3, 0):
    from collections.abc import Mapping

    def _get_iterator(d):
        return d.items()


else:
    from collections import Mapping

    def _get_iterator(d):
        return d.iteritems()


def merge(d, u):
    if not isinstance(d, Mapping):
        return d
    for k, v in _get_iterator(u):
        if isinstance(v, Mapping):
            d[k] = merge(d.get(k, {}), v)
        else:
            d[k] = v
    return d
