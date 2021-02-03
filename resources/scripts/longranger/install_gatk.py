#!/usr/bin/python3
# FIXME need a little work like REMOTE SOFTWARE URL
# REQUIRES /apps path to be created

import os, subprocess, sys, yaml

APPS_DIR = os.path.join(os.path.sep, "apps")

def install_gatk():
    sys.stderr.write("Install GATK...\n")

    if os.path.isdir(APPS_DIR + '/gatk-4.0.0'):
        sys.stderr.write("GATK already installed...\n")
        return

    # FIXME verify
    cmd = ["apt-get", "install", "-y", "java-1.8.0-openjdk.x86_64"] # java8 for gatk4
    sys.stderr.write(f"RUNNING: {' '.join(cmd)}\n")
    subprocess.check_call(cmd)

    # FIXME need software location or ability to download
    conf = yaml.safe_load(open( os.path.join(APPS_DIR, "tenx", "config.yaml") ))
    install_gatk(conf['TENX_...'])

    os.chdir(APPS_DIR)
    gatk_zip = 'gatk-4.0.0.0.zip'
    gatk_url = os.path.join(REMOTE_DATA_URL, "software", gatk_zip)
    sys.stderr.write(f"Download GATK from {gatk_url}\n")
    while subprocess.call(['gsutil', '-m', 'cp', gatk_url, '.']):
        sys.stderr.write("Failed to download GATK! Trying again in 5 seconds...\n")
        time.sleep (5)

    assert os.path.exists(gatk_zip), "Failed to find DL'd GATK!"
    sys.stderr.write(f"Found GATK: {gatk_zip}\n")

    sys.stderr.write("UNZIP GATK...\n")
    while subprocess.call(['bsdtar', 'zxf', gatk_zip]):
        sys.stderr.write("Failed to unzip the GATK zip! Trying again in 5 seconds...\n")
        time.sleep (5)
    os.remove(gatk_zip)
    os.chdir('/')
    sys.stderr.write("Install gatk...OK\n")
#-- install_gatk

if __name__ == '__main__':
    install_gatk()
