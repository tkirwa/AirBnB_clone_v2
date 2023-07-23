#!/usr/bin/python3
"""Compress web static package
"""
from datetime import datetime
from os import path
from os.path import exists

from fabric.api import *

env.hosts = ['34.204.95.241', '52.87.230.196']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Fabric script that generates a .tgz archive from the contents
    of the web_static folder"""
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        # Upload archive
        print("Uploading archive...")
        put(archive_path, '/tmp/')

        # Get the filename without the extension
        filename = path.basename(archive_path).split(".")[0]

        # Create target dir
        print("Creating target directory...")
        run('mkdir -p /data/web_static/releases/{}/'.format(filename))

        # Uncompress archive and delete .tgz
        print("Uncompressing archive...")
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove archive
        print("Removing archive...")
        run('rm /tmp/{}.tgz'.format(filename))

        # Move contents into host web_static
        print("Moving contents to target directory...")
        run('mv -n /data/web_static/releases/{}/web_static/*'
            ' /data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove extraneous web_static dir
        print("Cleaning up extraneous directory...")
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))

        # Delete pre-existing symbolic link
        print("Removing existing symbolic link...")
        run('rm -rf /data/web_static/current')

        # Re-establish symbolic link
        print("Creating new symbolic link...")
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename))

        print("New version deployed!")
        # Return True on success
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False


def deploy():
    """Create and distribute an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False

    new_file = "web_static/my_index.html"
    local("echo \"<html><head></head><body>"
          "New version deployed!</body></html>\" > {}"
          .format(new_file))

    return do_deploy(archive_path)
