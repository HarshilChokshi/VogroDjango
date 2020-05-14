python3 ~/VogroDjango/manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > /tmp/datadump.json
gzip /tmp/datadump.json
