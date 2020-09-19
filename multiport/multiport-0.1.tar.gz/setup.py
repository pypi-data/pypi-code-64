from setuptools import setup, find_packages

setup(
    name="multiport",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "tqdm"],
    entry_points="""
        [console_scripts]
        multiport=multiport.cmd:multiport
    """,
)