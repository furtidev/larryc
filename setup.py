from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.3'
DESCRIPTION = 'Dictionary for your terminal'

with open('README.md', 'r+') as ld:
    LONG_DESCRIPTION = ld.read()

# Setting up
setup(
    name="larry",
    version=VERSION,
    author="furtidev (Isfer Hossain)",
    author_email="<megaphone@poto.cafe>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['rich'],
    keywords=['python', 'dictionary', 'cli', 'app', 'foss'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
