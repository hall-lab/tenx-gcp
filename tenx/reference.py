#!/usr/bin/env python

import glob, os, subprocess, sys
from app import TenxApp

class TenxReference():

    def __init__(self, name):
        self.name = name

    def references_directory(self):
        return os.path.join(os.path.sep, TenxApp.config['TENX_DATA_PATH'], 'references')

    def directory(self):
        return os.path.join(self.references_directory(), self.name)

    def genome_fasta_fn(self):
        return os.path.join(self.directory(), 'fasta', 'genome.fa')

    def tgz_bn(self):
        return ".".join([self.name, "tar", "gz"])

    def remote_url(self):
        return os.path.join(TenxApp.config['TENX_REMOTE_REFS_URL'], self.tgz_bn())

#-- TenxReference

def download(reference):
    sys.stderr.write("Downloading {0} reference from the object store...\n".format(reference.name))

    genome_fasta_fn = reference.genome_fasta_fn()
    sys.stderr.write("Reference: {0}\nFasta File: {1}\n".format(reference.name, genome_fasta_fn))
    if os.path.exists(genome_fasta_fn):
        sys.stderr.write("Reference already downloaded!")
        return

    refs_d = reference.references_directory()
    if not os.path.exists(refs_d): 
        os.makedirs(refs_d)

    rurl = reference.remote_url()
    sys.stderr.write("Checking for sample reference at {0} ...\n".format(rurl))
    subprocess.check_call(['gsutil',  'ls', rurl])

    pwd = os.getcwd()
    try:
        sys.stderr.write("Entering {0}\n".format(refs_d))
        os.chdir(refs_d)
        cmd = ['gsutil', 'cp', rurl, '.']
        sys.stderr.write("Running:  {0}\n".format(cmd))
        subprocess.check_call(cmd)
        tgz_bn = reference.tgz_bn()
        if not glob.glob(tgz_bn): raise Exception("Failed to download reference!")
        cmd = ['tar', '-zxvvf', tgz_bn]
        sys.stderr.write("Running:  {0}\n".format(cmd))
        rv = subprocess.check_call(cmd)
        os.remove(tgz_bn)
        if not glob.glob(genome_fasta_fn): raise Exception("Failed to find {} inside reference directory!".format(genome_fasta_fn))
    finally:
        os.chdir(pwd)

    sys.stderr.write("Downloading reference from the object store...OK\n")

#-- download
