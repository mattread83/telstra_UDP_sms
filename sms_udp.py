import requests
import json
import socket

APP_KEY = '' # Get from https://dev.telstra.com/user/me/apps
APP_SECRET = '' # Get from https://dev.telstra.com/user/me/apps


UDP_IP = "0.0.0.0"
UDP_PORT = 5007

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	string = data.decode("utf-8")
	number = string[:10]
	message = string[10:50]
	#print ("received data:", data)
	print ("received data:", string)
	print ("number:", number)
	print ("message:", message)
	
	tokenPayload = {'client_id' : APP_KEY,
                'client_secret': APP_SECRET,
                'grant_type' : 'client_credentials',
                'scope' : 'SMS'}

	request = "https://api.telstra.com/v1/oauth/token"
	response = json.loads(requests.get(request, params = tokenPayload).text)
	TOKEN = response['access_token']


	payload = {'to': number,
           'body': message}

		   
		   
	r = requests.post('https://api.telstra.com/v1/sms/messages', 
                  headers = {'Content-Type' : 'application/json',
                             'Authorization' : 'Bearer ' + TOKEN},
                  data = json.dumps(payload))

	print (r.text)
	print (r.status_code)