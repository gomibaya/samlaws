import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="samlaws",
    version="0.1.0b1",
    author="Esteban Barón",
    author_email="esteban@gominet.net",
    description="Configuracion aws cli en conexiones basadas en SAML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gomibaya/samlaws/",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'bs4',
        'boto3',
        'defusedxml'
        ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Spanish",
    ],
    python_requires='>=3.6',
)
