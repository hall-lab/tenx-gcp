# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('tenx/version.py') as f:
    exec(f.read())

tests_require = [
    "mock",
    "nose",
]
install_requires=[
    "click==7.0",
    "Jinja2>=2.10.1",
    "pyyaml==5.1",
    "tabulate",
]

setup(
    name='tenx',
    version=__version__,
    description='10X Genomics CLI',
    long_description=readme,
    author='Eddie Belter',
    author_email='ebetler@wustl.edu',
    license=license,
    url='https://github.com/hall-lab/tenx-gcp.git',
    installs_requires=installs_require,
    entry_points='''
        [console_scripts]
        tenx=tenx.cli:cli
    ''',
    setup_requires=["pytest-runner"],
    test_suite="nose.collector",
    tests_requires=tests_require,
    packages=find_packages(include=['tenx'], exclude=('tests', 'docs')),
    include_package_data=True,
    package_data={"tenx": ["job-templates/*"]}
)
