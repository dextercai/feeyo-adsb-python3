#Base On VariFlight ADS-B Script
#Edited By DexterCai
#Running with Python 3.8.0
import socket
import urllib.request as urllib2
import urllib
import sys
import configparser
import zlib
import base64
import os,uuid
import time

serverHost = '127.0.0.1'
serverPort = 30003

config = configparser.ConfigParser()
config.read(sys.path[0]+'/config.ini')

uuid_file=sys.path[0]+'/UUID'

if os.path.exists(uuid_file) :
        file_object = open(uuid_file)
        mid = file_object.read()
        file_object.close()
else :
        mid = uuid.uuid1().get_hex()[16:]
        file_object = open(uuid_file , 'w')
        file_object.write( mid )
        file_object.close()


sockobj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sockobj.connect((serverHost,serverPort))

def send_message(source_data):
	try:
		source_data=base64.b64encode(zlib.compress(source_data))
		f=urllib2.urlopen(url = config.get("global","sendurl"),data = urllib.parse.urlencode({'from':mid,'code':source_data}).encode('GBK'), timeout = 2)
		print("return: ")
		print(f.read())
		return True
	except Exception as e:
		print(str(e))
		return True

tmp_buf=bytes()
while 1:
	buf = sockobj.recv(1024)
	if not buf: break
	if len(buf) != 0:
		tmp_buf = tmp_buf + buf
		if buf[len(buf)-1] == 10:
			if send_message(tmp_buf) :
				tmp_buf=bytes()
				
time.sleep(0)
