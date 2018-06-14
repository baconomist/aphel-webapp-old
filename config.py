from json import load
from urllib.request import urlopen

DEBUG = False
ip = "127.0.0.1"
port = 80

if DEBUG:
    public_address = ip
else:
    public_address = "apheltech.ca"