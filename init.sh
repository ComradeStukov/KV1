# Generate config files from template.

cd database
cp create_database_template.sql create_database.sql
cp config_template.py config.py
cd ..

cd uwsgi
cp uwsgi_template.ini uwsgi.ini
cd ..

cd web_server
cp config_template.py config.py
cd ..

pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
