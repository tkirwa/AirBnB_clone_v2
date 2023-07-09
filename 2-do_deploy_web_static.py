#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from datetime import datetime
from os.path import exists

from fabric.api import env, put, run, task

env.hosts = ["34.204.95.241", "52.87.230.196"]
env.user = "ubuntu"


@task
def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        folder_name = file_name.split(".")[0]
        path_no_ext = "/data/web_static/releases/{}".format(folder_name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_no_ext))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path_no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv {}/web_static/* {}".format(path_no_ext, path_no_ext))
        run("rm -rf {}/web_static".format(path_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False


def do_pack():
    """Generates a .tgz archive"""
    try:
        from fabric.operations import local

        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None
