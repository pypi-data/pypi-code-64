from setuptools import setup
 
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Education",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3"
]

setup(
    name = 'zkdatabuilder',
    version = '0.0.1',
    description = 'Builds E.coli model with DNA, free and bound transcription factors data file for lammps mimicing real bp density of E.coli',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    py_modules = ["angler1","bonder","BuildNwrite","cap","cylinder",f"reeTF","membrane","position","radius"],
    package_dir = {'': 'src'},
    author='Zafer Kosar',
    author_email='zafer.kosar.physics@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='data file, lammps, lammps data file,E. coli model',
    install_requires= ['numpy']
)
