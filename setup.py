"""
Setup file for acme.

"""

from setuptools import setup, find_packages

setup(
    name="acme",
    project_urls={
        'Source': 'https://github.com/lincmba/acme',
    },
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        "amqp",
        "appnope",
        "asgiref",
        "backcall",
        "billiard",
        "celery",
        "certifi",
        "chardet",
        "click",
        "click-didyoumean",
        "click-plugins",
        "click-repl",
        "decorator",
        "Django",
        "idna",
        "importlib",
        "ipdb",
        "ipython",
        "ipython-genutils",
        "jedi",
        "kombu",
        "matplotlib-inline",
        "parso",
        "pep517",
        "pexpect",
        "pickleshare",
        "pip-tools",
        "prompt-toolkit",
        "psycopg2",
        "ptyprocess",
        "Pygments",
        "pytz",
        "requests",
        "six",
        "sqlparse",
        "toml",
        "traitlets",
        "unicodecsv",
        "urllib3",
        "vine",
        "wcwidth"
    ]
)
