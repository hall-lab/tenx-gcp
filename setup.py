# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('tenx/version.py') as f:
    exec(f.read())

setup(
    name='tenx',
    version=__version__,
    description='10X Genomics Pipeline Commands',
    long_description=readme,
    author='Eddie Belter',
    author_email='ebetler@wustl.edu',
    license=license,
    #url='https://github.com/ernfrid/cromwell_cost',
    install_requires=[
        'click==6.7',
        #'clint==0.5.1',
        #'google-api-python-client==1.7.3',
        #'google-auth==1.5.1',
        #'python-dateutil==2.7.3',
        #'requests==2.20.0',
        #'tabulate==0.8.2',
        #'cytoolz==0.9.0.1',
        #'toolz==0.9.0',
        #'PyMySQL==0.9.3',
        #'pyparsing==2.3.1',
        #'pyhocon==0.3.51'
    ],
    entry_points='''
        [console_scripts]
        tenx=tenx.cli:cli
    ''',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
)
