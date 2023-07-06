#!/usr/bin/python3
from datetime import datetime

from fabric.api import local


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()

    # Create a formatted date string for the archive name
    dt_string = now.strftime("web_static_%Y%m%d%H%m%S")

    # Set the output file path and name
    output_file = "versions/{:}.tgz".format(dt_string)

    # Create the 'versions' directory if it doesn't exist
    local("mkdir -p versions")

    # Compress the 'web_static' folder into the output file
    result = local("tar -cvzf {:} web_static".format(output_file))

    # Check if the compression was successful
    if result.failed:
        return None

    # Return the path to the created archive
    return output_file
