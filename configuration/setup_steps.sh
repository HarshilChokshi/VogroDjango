# Setup script to setup Django, MySQL, and dependencies on server

# Command to dump data from current database
python3 manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > /tmp/datadump.json

# Install all packages/dependencies
sudo apt-get update
sudo apt install python3-pip
pip3 install "django==3.0.5"
pip3 install "geopy==1.21.0"
pip3 install "django-crontab==0.7.1"
pip3 install "djangorestframework==3.11.0"
sudo apt install mysql-server
sudo apt install libmysqlclient-dev default-libmysqlclient-dev
pip3 install "mysqlclient==1.4.6"
pip3 install "gunicorn==20.0.4"
sudo apt-get install nginx

# Setup database and db user
sudo mysql -u root
CREATE DATABASE vogro_api;
create user 'django'@'localhost' identified by ‘Vogro2020’;
grant usage on *.* to 'django'@'localhost';
grant all privileges on vogro_api.* to 'django'@'localhost';
FLUSH PRIVILEGES;

#Setup nginx
sudo mv ~/VogroDjango/configuration/djtrump /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/djtrump /etc/nginx/sites-enabled
#Command to check if setup is good so far
sudo nginx -t


# Copy over code, start db, and django server
scp -r ~/VogroDjango/ ubuntu@ec2-13-59-38-83.us-east-2.compute.amazonaws.com:/home/ubuntu
sudo touch /etc/mysql/my.cnf
add config data
sudo systemctl daemon-reload
sudo systemctl restart mysql
python3 manage.py migrate
python3 manage.py loaddata /tmp/datadump.json
gunicorn --daemon --bind unix:/home/ubuntu/VogroDjango/VogroDjango.sock VogroDjango.wsgi > /tmp/django-output.log
sudo service nginx restart
python3 manage.py crontab add
