# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_genomics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pandas-genomics',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'John McGuigan',
    'author_email': 'jrm5100@psu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
