#!/usr/bin/env bash
hg pull -u https://thetoxickiller:bItbucket40@bitbucket.org/apheltech/webapp/src/default/ -r release
hg update

sudo kill `sudo lsof -t -i:80`

source /home/webapp/webappenv/bin/activate
pip install -r /home/webapp/requirements.txt

uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi

