#!/usr/bin/python3
"""
A Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""

from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ["34.204.95.241", "52.87.230.196"]  # <IP web-01>, <IP web-02>


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.split('.')[0]
        release_path = "/data/web_static/releases/{}".format(folder_name)

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        
        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_path))
        
        # Remove the uploaded archive from the web server
        run("rm /tmp/{}".format(file_name))
        
        # Move the contents of the uncompressed folder to the release folder
        run("mv {}/web_static/* {}".format(release_path, release_path))
        
        # Remove the unnecessary web_static folder
        run("rm -rf {}/web_static".format(release_path))
        
        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")
        
        # Create a new symbolic link to the new release folder
        run("ln -s {} /data/web_static/current".format(release_path))
        
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False
