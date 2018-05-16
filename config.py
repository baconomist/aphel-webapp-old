from json import load
from urllib.request import urlopen

DEBUG = False
ip = "127.0.0.1"
port = 80
public_address = load(urlopen('http://jsonip.com'))['ip'] + str(port)
