#!/usr/bin/python3

import os, shutil, subprocess

def end_motd():
    f = open('/etc/motd', 'w')
    f.write('')
    f.close()

    msg = """
*** LONGRANGER AND TENX INSTALLATION COMPLETE ***
***        YOU MAY NEED TO LOG OUT/IN        ***
"""
    subprocess.call(['wall', '-n', msg])
#-- end_motd

if __name__ == '__main__':
    end_motd()
