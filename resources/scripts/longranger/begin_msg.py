#!/usr/bin/python3

import os, shutil

def start_motd():
    if os.path.exists("/etc/motd"):
        shutil.copy("/etc/motd", "/etc/motd.bak") 

    msg = """
***    LONGRANGER AND TENX IS CURRENTLY BEING INSTALLED/CONFIGURED IN THE BACKGROUND  ***
***                 A TERMINAL BROADCAST WILL ANNOUNCE WHEN COMPLETE                  ***
*** IF THIS MESSAGE PERSISTS FOR AN UNEXPECTED AMOUNT OF TIME, CONTACT YOUR SYS ADMIN ***
"""
    f = open('/etc/motd', 'w')
    f.write(msg)
    f.close()

#-- start_motd()

if __name__ == '__main__':
    start_motd()
