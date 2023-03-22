# setup.py

from setuptools import setup

setup(
    name='certifycert',
    version='0.1.0',
    install_requires=[
          'certifi', 'ocsp_checker', 'pyopenssl', 'requests', 'pyjarm', 'termcolor'
      ],
    )
