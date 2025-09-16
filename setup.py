from setuptools import setup

setup(
    name="unicodec",
    version="0.1.1",
    packages=["unicodec"],
    install_requires=[
        "six",
        'typing-extensions; python_version <= "2.7"',
    ],
)
