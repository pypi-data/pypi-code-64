import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ArabicOcr", # Replace with your own username
    version="1.1.6",
    author="Falah.G.Saleh",
    author_email="falahgs07@gmail.com",
    description="Python package to convert Arabic images to text by OCR technique detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://iraqprogrammer.wordpress.com/",
    packages=["ArabicOcr"],
	keywords = ['arabic ocr', 'images', 'dataset images'],
	install_requires=[            # I get to this in a second
          	'easyocr',
			      ],
    classifiers=[
        "Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)