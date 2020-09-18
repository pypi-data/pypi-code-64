import os as _os

_tmp = {}
exec("from os import *", _tmp)
from os import *

# shadowing os with local definitions
from .path import *
from . import path

sep = '/'

__all__=list(_tmp.keys())