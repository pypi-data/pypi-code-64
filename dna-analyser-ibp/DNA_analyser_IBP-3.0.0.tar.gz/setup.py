# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['DNA_analyser_IBP',
 'DNA_analyser_IBP.adapters',
 'DNA_analyser_IBP.interfaces',
 'DNA_analyser_IBP.intersection',
 'DNA_analyser_IBP.models',
 'DNA_analyser_IBP.ports']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'pandas>=1.1.2,<2.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.24.0,<3.0.0',
 'tenacity>=6.2.0,<7.0.0',
 'tqdm>=4.49.0,<5.0.0']

setup_kwargs = {
    'name': 'dna-analyser-ibp',
    'version': '3.0.0',
    'description': 'DNA analyser API wrapper tool for Jupiter notebooks.',
    'long_description': '<div align="center">\n    <img src="https://gitlab.com/PatrikKaura/dna_analyser_ibp_logos/-/raw/master/logo.png" alt=\'logo\' width=\'300px\'>\n    <br/>\n    <br/>\n    <img src="https://img.shields.io/badge/version-3.0.0-brightgreen.svg" alt=\'version\'/>\n    <img src="https://img.shields.io/badge/python-3.6-brightgreen.svg" alt=\'python_version\'/>\n    <img src="https://img.shields.io/badge/python-3.7-brightgreen.svg" alt=\'python_version\'/>\n    <img src=\'https://img.shields.io/badge/licence-GNU%20v3.0-blue.svg\' alt=\'licence\'/>\n    <h1 align=\'center\'> DNA analyser IBP </h1>\n</div>\n\n\nTool for creating Palindrome, P53predictor, and G4Hunter analysis. Work as API wrapper for IBP DNA analyzer API [bioinformatics.ibp](http://bioinformatics.ibp.cz/).\nCurrently working with an instance of DNA analyser server running on http://bioinformatics.ibp.cz computational core but can be switched \nto the local instance of the server.\n\n# Getting Started\n\n## Prerequisites\n\npython >= 3.6\n\n## Installing\n\nTo install test version from [Pypi](https://pypi.org/project/dna-analyser-ibp/).\n\n```commandline\npipenv install dna-analyser-ibp\n```\n\n```commandline\npip install dna-analyser-ibp\n```\n\n## Documentation\n\nMethods are documented in the following [documentation](https://patrikkaura.gitlab.io/DNA_analyser_IBP/).\n\n## Quick start\n\nDNA analyser uses `pandas.Dataframe` or `pandas.Series`. Firstly the user  has to create `Api` object and login to API.\n```python\nfrom DNA_analyser_IBP.api import Api\n\nAPI = Api()\n```\n```python\nEnter your email        example@example.cz\nEnter your password     ········\n\n2020-09-16 18:51:17.943398 [INFO]: User host is trying to login ...\n2020-09-16 18:51:17.990580 [INFO]: User host is successfully loged in ...\n```\nIf DNA analyser API server not running on http://bioinformatics.ibp.cz then use this example to create `Api` object.\n```python\nfrom DNA_analyser_IBP.api import Api\n\nAPI = Api(server=\'http://hostname:port/api\')\n```\nThen upload NCBI sequence for example `Homo sapiens chromosome 12` use.\n```python\nAPI.sequence.ncbi_creator(circular= True, tags=[\'Homo\',\'sapiens\', \'chromosome\'], name=\'Homo sapiens chromosome 12\', ncbi_id=\'NC_000012.12\')\n```\nTo analyse NCBI sequence use g4hunter interface.\n```python\nsapiens_sequence = API.sequence.load_all(tags=\'Homo\') # get series with sapiens sequence\n\n# run g4hunter analyses with these params\nAPI.g4hunter.analyse_creator(sequence=sapiens_sequence, tags=[\'testovaci\',\'Homo\', \'sapiens\'], threshold=1.4, window_size=30)\n```\nLast step to see results of g4hunter analysis.\n```python\nsapiens = API.g4hunter.load_all(tags=[\'Homo\']) # returns dataframe\nAPI.g4hunter.load_results(analyse=sapiens.iloc[0]) # iloc[0] to select row from dataframe\n```\n## P53 / G4KILLER TOOL\nTo run simple tools using plain text input.\n```python\n# implements g4killer algorithm for generating sequence with lower gscore\nAPI.g4killer.run(sequence=\'AATTATTTGGAAAGGGGGGGTTTTCCGA\', threshold=0.5) \n\n# implements calculations of p53 binding predictor for 20 base pairs sequences \nAPI.p53.run(sequence=\'GGACATGCCCGGGCATGTCC\') \n```\n\n# Development\n\n## Dependencies\n\n* tenacity >= 6.1.0\n* requests >= 2.20\n* requests-toolbelt >= 0.9.1\n* pyjwt >= 1.7.1\n* pandas >= 0.23\n* matplotlib >= 3.0.3\n* tqdm >= 4.28\n\n## Tests\n\nTo run tests only when downloaded directly from this repository.\n\n```commandline\npytest -v tests/\n```\n\n## Authors\n\n* **Patrik Kaura** - *Main developer* - [patrikkaura](https://gitlab.com/PatrikKaura/)\n* **Jan Kolomaznik** - *Supervisor* - [jankolomaznik](https://github.com/Kolomaznik)\n* **Jiří Šťastný** - *Supervisor*\n\n## License\n\nThis project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details.\n',
    'author': 'Patrik Kaura',
    'author_email': 'patrikkaura@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/PatrikKaura/DNA_analyser_IBP/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
