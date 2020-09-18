from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name="root_finding-pkg-thanjira", # Replace with your own username
  version='0.0.4',
  description='Root-Finding optimization',
  long_description=open('README.txt').read() ,
  url='',  
  author='Thanjira Pornsasawat',
  author_email='tp1u19@soton.ac.uk',
  license='MIT', 
  classifiers=classifiers,
  keywords=['goldenSection', 'bisection', 'newton', 'secant', 'brent', 'quasi-newton', 'trust region'],
  packages=find_packages(),
  install_requires=[''] 
)