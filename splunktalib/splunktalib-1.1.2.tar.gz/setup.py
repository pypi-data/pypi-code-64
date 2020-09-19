# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunktalib',
 'splunktalib.common',
 'splunktalib.concurrent',
 'splunktalib.conf_manager',
 'splunktalib.httplib2_helper',
 'splunktalib.httplib2_helper.httplib2_py2',
 'splunktalib.httplib2_helper.httplib2_py2.httplib2',
 'splunktalib.httplib2_helper.httplib2_py3',
 'splunktalib.httplib2_helper.httplib2_py3.httplib2',
 'splunktalib.schedule']

package_data = \
{'': ['*']}

install_requires = \
['httplib2>=0,<1', 'sortedcontainers>=2.2,<3.0']

setup_kwargs = {
    'name': 'splunktalib',
    'version': '1.1.2',
    'description': 'Supporting library for Splunk Add-ons',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
