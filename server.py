import socket
import json
import sys

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      

udp_host = socket.gethostname()		        
udp_port = 12345			                


# list of registered users
registered_users =[]

sock.bind((udp_host,udp_port))

#Register user if user is not yet in the list of clients and return appropriate response
# to the client
def register_user(request):
	if request['handle'] in registered_users:
		error = {
			"command": 'error',
			"message": 'Error: Registration failed, handle or alias already exists'
		}
		
		return error
	else:
		registered_users.append(request['handle'])

		#unsure about the implementation of this since theres no explicit "command: success"
		# in the MP specs
		success = {
			"command": 'success',
			"message": 'Registration successful. Welcome ' + request['handle']
		}

		print('Current list of registered users: ', registered_users)
		return success


		



while True:
	print ("Waiting for client request...")
	
	data,client_addr = sock.recvfrom(1024)	  
	    
	#convert data in JSON to python dictionary
	dict_req = json.loads(data)

	if dict_req['command'] == "register":

		#process registration, results are in the form of a dict
		res = register_user(dict_req)

		print('registered dic response', res)
		#convert dictionary to JSON (for interpoability), encode into bytes
		json_response = json.dumps(res).encode('utf-8')
		
      
		sock.sendto(json_response,client_addr)


	
	#print('dict_req', dict_req)
	#print(type(dict_req))
	#print(dict_req['command'])


