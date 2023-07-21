#!/usr/bin/python3
"""
This module contains the function do_pack that generates a .tgz archive
from the contents of the web_static folder (fabric script)
"""

import os
from datetime import datetime

from fabric.api import env, local, put, run

# Update these values with the appropriate IP addresses...
#  and username for your servers
env.hosts = ['34.204.95.241', '52.87.230.196']
env.user = 'ubuntu'


def do_pack():
    """Fabric script that generates a .tgz archive from the contents
    of the web_static folder"""
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date)
        result = local("tar -czvf {} web_static/".format(archive_path))

        if result.succeeded:
            return archive_path
        else:
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def do_deploy(archive_path):
    """Fabric script to distribute an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on each server
        put(archive_path, "/tmp/")
        # Get the filename without the extension
        filename = os.path.basename(archive_path).split(".")[0]
        # Create the release directory on the server
        run("mkdir -p /data/web_static/releases/{}/".format(filename))
        # Uncompress the archive into the release directory
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(filename, filename))
        # Remove the uploaded archive from /tmp/
        run("rm /tmp/{}.tgz".format(filename))

        # Additional commands to forcefully remove existing files/directories
        run("find /data/web_static/releases/{}/web_static/"
            " -type f -not -name '.*' -delete"
            .format(filename))
        run("find /data/web_static/releases/{}/web_static/"
            " -type d -empty -delete"
            .format(filename))

        # Use rsync to move the contents of the release directory
        #  to the parent directory
        run("rsync -a /data/web_static/releases/{}/web_static/"
            " /data/web_static/releases/{}/"
            .format(filename, filename))
        # Remove the now empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        # Delete the old symbolic link
        run("rm -rf /data/web_static/current")
        # Create a new symbolic link pointing to the latest release
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        print("New version deployed!")
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False


# if __name__ == "__main__":
#     # Pack the web_static folder and get the path of the archive
#     archive_path = do_pack()
#     if archive_path:
#         # Deploy the archive to the web servers
#         do_deploy(archive_path)
