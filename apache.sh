#!/bin/bash

sudo apt -y install python3
sudo apt -y install python3-pip
sudo apt -y install apache2
sudo apt -y install libapache2-mod-wsgi-py3

sudo pip3 install flask

sudo apt -y install git 

git clone https://gitlab.com/sshguru/pyraces

sudo ln -sT ~/pyraces /var/www/html/pyraces

cat >> /etc/apache2/sites-enabled/000-default.conf<< EOF
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
	ServerName web

        WSGIDaemonProcess flaskapp threads=5
        WSGIScriptAlias / /var/www/html/pyraces/pyraces.wsgi
        WSGIApplicationGroup %{GLOBAL}
        <Directory pyraces>
             WSGIProcessGroup pyraces
             WSGIApplicationGroup %{GLOBAL}
             Order deny,allow
             Allow from all 
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
         Header set Access-Control-Allow-Origin "*"
</VirtualHost>
EOF

sudo service apache2 restart