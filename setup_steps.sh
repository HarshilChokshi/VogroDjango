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

# Setup database and db user
sudo mysql -u root
CREATE DATABASE vogro_api;
create user 'django'@'localhost' identified by ‘Vogro2020’;
grant usage on *.* to 'django'@'localhost';
grant all privileges on vogro_api.* to 'django'@'localhost';
FLUSH PRIVILEGES;

# Copy over code, start db, and django server
scp -r ~/VogroDjango/ ubuntu@ec2-13-59-38-83.us-east-2.compute.amazonaws.com:/home/ubuntu
sudo touch /etc/mysql/my.cnf
add config data
sudo systemctl daemon-reload
sudo systemctl restart mysql
python3 manage.py migrate
python3 manage.py loaddata /tmp/datadump.json
nohup python3 manage.py runserver ec2-13-59-38-83.us-east-2.compute.amazonaws.com:8000 > /tmp/django-output.log &
python3 manage.py crontab add
