#!/usr/bin/python3
"""This module contains the function do_pack that generates a .tgz archive
from the contents of the web_static folder (fabric script)"""

from datetime import datetime

from fabric.api import *


def do_pack():
    """Fabric script that generates a .tgz archive from the contents
    of the web_static folder"""
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(date)
        # result = local("tar -cvzf {} -C web_static".format(filename))
        result = local("tar -cvzf {} -C web_static .".format(filename))

        if result.succeeded:
            return filename
        else:
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None
