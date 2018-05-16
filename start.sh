sudo kill `sudo lsof -t -i:80`
uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi