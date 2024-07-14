#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:number=2
    -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['100.26.168.62', '52.201.185.25']

def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)

    # Local cleaning
    archives_local = sorted(os.listdir("versions"))
    if number >= 0:
        archives_to_keep_local = archives_local[-number:]
    else:
        archives_to_keep_local = []

    with lcd("versions"):
        for archive in archives_local:
            if archive not in archives_to_keep_local:
                local("rm -rf {}".format(archive))

    # Remote cleaning
    with cd("/data/web_static/releases"):
        archives_remote = run("ls -tr").split()
        archives_to_delete_remote = []
        if number > 0:
            archives_to_delete_remote = archives_remote[:-number]

        for archive in archives_to_delete_remote:
            run("rm -rf {}".format(archive))
