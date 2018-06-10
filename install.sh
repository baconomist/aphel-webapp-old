sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update

sudo apt-get install python3.6
sudo apt-get install python3.6-dev
sudo apt-get install python3.6-venv

wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py

sudo apt-get install mercurial

virtualenv /home/webapp/webappenv/

source /home/webapp/start.sh
