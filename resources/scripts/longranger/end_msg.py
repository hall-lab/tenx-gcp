#!/usr/bin/env python

import os, shutil

def end_motd():
    if os.path.exists("/etc/motd.bak"):
        shutil.copy("/etc/motd.bak", "/etc/motd") 
    else:
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
