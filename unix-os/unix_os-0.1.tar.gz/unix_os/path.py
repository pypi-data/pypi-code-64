import os as _os
from os.path import *


def join(a, *p):
    return '/'.join([a] + list(p))


join.__doc__ = _os.path.join.__doc__


for item in ['normpath', 'abspath']:
    exec(f'''
def {item}(path):
    return _os.path.{item}(path).replace('\\\\', '/')

{item}.__doc__ = _os.path.{item}.__doc__
''')


