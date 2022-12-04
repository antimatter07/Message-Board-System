import socket
import json
import sys
import queue
import threading

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      
udp_host = socket.gethostname()		        
udp_port = 12345			                

messages = queue.Queue()

print("Server is online.")
print("Waiting for clients...")

# list of registered users
# Registered users are stored as {username: <name>, address: <address>}
registered_users = []

sock.bind((udp_host,udp_port))

#Register user if user is not yet in the list of clients and return appropriate response to the client
def register_user(request, address):
	# Also prevents repeated registering
	if isRegistered(request['handle'], address):
		error = {
			"command": 'error',
			"message": 'Error: Registration failed, handle or alias already exists'
		}
		
		return error

	else:
		registered_users.append({ "username": request['handle'], "address": address})
		success = {
			"command": 'success',
			"message": 'Registration successful. Welcome ' + request['handle']
		}

		print('Current list of registered users: ', registered_users[0]['username'])
		return success


# Stores all sent messages into a queue
def receiveMessages():
	while True:
		try:
			msg, adr = sock.recvfrom(1024)

			dict_req = json.loads(msg)

			messages.put([dict_req, adr])
		except:
			print("Error with storing message")


# Repeatedly executes the messages/commands if listed
def broadcastMessages():
	while True:
		# Loops through the messages queue
		while not messages.empty():
			q = messages.get()
			message = q[0]
			address = q[1]
				
			if message['command'] == "register":
				#process registration, results are in the form of a dict
				res = register_user(message, address)

				#convert dictionary to JSON (for interpoability), encode into bytes
				json_response = json.dumps(res).encode('utf-8')
			
				sock.sendto(json_response, address)

			elif message['command'] == "all":
				pass

			elif message['command'] == "msg":
				pass

			elif message['command'] == "join":
				pass

			elif message['command'] == "leave":
				pass


# Check if user is registered
def isRegistered(username, address):
	for user in registered_users:
		if user['username'] == username or user['address'] == address:
			return True

	return False

			
receiving_thread = threading.Thread(target=receiveMessages)
broadcast_thread = threading.Thread(target=broadcastMessages)

receiving_thread.start()
broadcast_thread.start()