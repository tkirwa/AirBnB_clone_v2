from fabric import task
from datetime import datetime
from fabric.api import local
from os.path import isdir


@task
def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        output_file = "versions/web_static_{}.tgz".format(dt_string)
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(output_file))
        return output_file
    except Exception as e:
        print("An error occurred:", str(e))
        return None
