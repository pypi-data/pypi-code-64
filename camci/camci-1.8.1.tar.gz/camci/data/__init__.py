# -*- coding: utf-8 -*-

from camci import config
from camci.data.base import DataHandler, register_sources

register_sources()
handler = DataHandler(*config.data_sources)
