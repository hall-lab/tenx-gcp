#!/usr/bin/python3

import subprocess

def begin_msg():
    msg = """
***    LONGRANGER AND TENX IS CURRENTLY BEING INSTALLED/CONFIGURED IN THE BACKGROUND  ***
***                 A TERMINAL BROADCAST WILL ANNOUNCE WHEN COMPLETE                  ***
*** IF THIS MESSAGE PERSISTS FOR AN UNEXPECTED AMOUNT OF TIME, CONTACT YOUR SYS ADMIN ***
"""
    f = open('/etc/motd', 'w')
    f.write(msg)
    f.close()
#-- begin_msg()

def end_msg():
    f = open('/etc/motd', 'w')
    f.write('')
    f.close()

    msg = """
*** LONGRANGER AND TENX INSTALLATION COMPLETE ***
***        YOU MAY NEED TO LOG OUT/IN        ***
"""
    subprocess.call(['wall', '-n', msg])
#-- end_msg
