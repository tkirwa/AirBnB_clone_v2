#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
import os
from fabric.api import env, run, put
from datetime import datetime


env.hosts = ["34.204.95.241", "52.87.230.196"]
env.user = 'ubuntu'


def do_pack():
    """Creates a compressed archive of web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    local("mkdir -p versions")
    local("tar -czvf {} web_static".format(archive_path))
    return archive_path


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Get file name
        file_name = os.path.basename(archive_path)

        # Upload archive to /tmp/ directory on the server
        put(archive_path, "/tmp/{}".format(file_name))

        # Create folder to extract archive
        release_folder = "/data/web_static/releases/{}".format(file_name[:-4])
        run("mkdir -p {}".format(release_folder))

        # Extract the contents of the archive to the folder
        run("tar -xzf /tmp/{} -C {}".format(file_name, release_folder))

        # Delete the archive file
        run("rm /tmp/{}".format(file_name))

        # Move the contents of the extracted folder to the release folder
        run("mv {}/web_static/* {}".format(release_folder, release_folder))

        # Remove the empty web_static folder
        run("rm -rf {}/web_static".format(release_folder))

        # Delete the symbolic link if it exists
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(release_folder))

        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
