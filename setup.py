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
    description='10X Genomics CLI',
    long_description=readme,
    author='Eddie Belter',
    author_email='ebetler@wustl.edu',
    license=license,
    url='https://github.com/hall-lab/tenx-gcp.git',
    install_requires=[
        'click==7.0',
        'pyyaml==5.1',
        'Jinja2>=2.10.1',
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
