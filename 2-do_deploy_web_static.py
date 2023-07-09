#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["34.204.95.241", "52.87.230.196"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to the /tmp/ directory of the web server
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False

    # Remove existing release folder
    if run("rm -rf /data/web_static/releases/{}/"
           .format(name)).failed is True:
        return False

    # Create the release directory
    if run("mkdir -p /data/web_static/releases/{}/"
           .format(name)).failed is True:
        return False

    # Uncompress the archive to the release directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
           .format(file, name)).failed is True:
        return False

    # Remove the uploaded archive from the web server
    if run("rm /tmp/{}".format(file)).failed is True:
        return False

    # Move the contents of the uncompressed folder to the release directory
    mv_command = "mv /data/web_static/releases/{}/web_static/* " \
        "/data/web_static/releases/{}/".format(name, name)
    if run(mv_command).failed is True:
        return False
    
    # Remove the empty web_static directory
    if run("rm -rf /data/web_static/releases/{}/web_static"
           .format(name)).failed is True:
        return False

    # Remove the current symbolic link
    if run("rm -rf /data/web_static/current").failed is True:
        return False

    # Create a new symbolic link to the new release folder
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
           .format(name)).failed is True:
        return False

    return True
