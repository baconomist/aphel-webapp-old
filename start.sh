sudo kill `sudo lsof -t -i:80`

source /home/webapp/webappenv/bin/activate
pip install -r /home/webapp/requirements.txt

uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi