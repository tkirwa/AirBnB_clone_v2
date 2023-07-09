#!/usr/bin/env bash

# Install Nginx if it's not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders if they don't exist
web_static_dir="/data/web_static"
releases_dir="$web_static_dir/releases"
shared_dir="$web_static_dir/shared"
test_dir="$releases_dir/test"
index_file="$test_dir/index.html"

sudo mkdir -p "$web_static_dir"
sudo mkdir -p "$releases_dir"
sudo mkdir -p "$shared_dir"
sudo mkdir -p "$test_dir"

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > "$index_file"

# Create or update symbolic link
symbolic_link="/data/web_static/current"
if [ -L "$symbolic_link" ]; then
    sudo rm "$symbolic_link"
fi
sudo ln -s "$test_dir" "$symbolic_link"

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu "/data/"

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sudo sed -i 's/^\(\s*location \/ {\)$/\1\n\t\talias \/data\/web_static\/current\/;/' "$config_file"

# Restart Nginx
sudo service nginx restart

exit 0
