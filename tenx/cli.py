from __future__ import print_function

import click

from tenx.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    '''
    10X Geomics Pipelines, Scripts, and Helpers
    '''

