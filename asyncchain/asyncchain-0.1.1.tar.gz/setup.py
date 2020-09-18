# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncchain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncchain',
    'version': '0.1.1',
    'description': 'Small python library to allow "async chaining"',
    'long_description': '# asyncchain\nSmall python library to allow "async chaining"\n\n\n## Usage\n```py\nimport asyncio\n\nfrom asyncchain import ChainMeta\n\n\nclass Target(metaclass=ChainMeta):\n    async def first(self):\n        print("first")\n\n    async def second(self):\n        print("second")\n\n\nasync def main():\n    my_target = Target()\n\n    await my_target.first().second()\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n',
    'author': 'StarrFox',
    'author_email': 'starrfox6312@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/StarrFox/asyncchain',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
