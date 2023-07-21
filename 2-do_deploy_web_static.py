#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from os import path

env.hosts = ['34.204.95.241', '52.87.230.196']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        if not (path.exists(archive_path)):
            return False

        # Upload archive
        put(archive_path, '/tmp/')

        # Get the filename without the extension
        filename = path.basename(archive_path).split(".")[0]

        # Create target dir
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(filename))

        # Uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove archive
        run('sudo rm /tmp/{}.tgz'.format(filename))

        # Move contents into host web_static
        run('sudo mv -n /data/web_static/releases/{}/web_static/*'
            ' /data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename))

        print("New version deployed!")
        # Return True on success
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False
