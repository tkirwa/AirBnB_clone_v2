#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

sudo apt-get -y update
# Install Nginx if it is not already installed
sudo apt-get -y install nginx
# Create the folder /data/ if it doesn’t already exist
# Create the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
# Create the folder /data/web_static/shared/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# echo "This is a test" | sudo tee /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# The command chown -hR is used to change the ownership of files and directories recursively
# sudo chown -hR ubuntu:ubuntu /data/

sudo chown -hR ubuntu:ubuntu /data/
# This command inserts the following block of text at line 38 of the
# /etc/nginx/sites-available/default file
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
# Restart Nginx after updating the configuration
sudo service nginx restart
