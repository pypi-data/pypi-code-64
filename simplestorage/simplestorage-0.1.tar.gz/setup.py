from setuptools import setup


setup(name='simplestorage',
      version='0.1',
      description='Storage client for local and gcloud',
      url='https://github.com/tbchk/simple-storage',
      download_url='https://github.com/tbchk/simple-storage/archive/0.1.tar.gz',
      author='Juan F. Hernandez',
      author_email='jhernandez426@gmail.com',
      license='MIT',
      packages=['simplestorage'],
      keywords=['google', 'cloud', 'storage', 'local'],
      install_requires=[
          'google-cloud-storage',
          'pydantic'
      ],
      zip_safe=False)