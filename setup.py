from setuptools import setup

setup(
    name="unicodec",
    version="0.2.0",
    packages=["unicodec"],
    install_requires=[
        "six",
        'typing-extensions; python_version <= "2.7"',
    ],
)
