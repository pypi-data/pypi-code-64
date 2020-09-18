import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mintpy_beta-meissam", # Replace with your own username
    version="0.0.1",
    author="Meissam Mehdizadeh",
    author_email="meissam.mehdizadeh@gmail.com",
    description="MintPy Beta Version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehdizadehm/MintPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
