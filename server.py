import socket
import json
import sys
import queue
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      
udp_host = socket.gethostbyname(socket.gethostname())	        
udp_port = 12345			                

messages = queue.Queue()

# List of connected port numbers
addresses = []

# list of users
# Registered users are stored as {username: <name>, address: <address>}
registered_users = []

server.bind((udp_host,udp_port))

print("Server is online.")
print("Waiting for clients...")

#Add address to list of users in the server
def join_user(address):
	# Check if port address is already used
	if isConnected(address):
		error = {
		"command": 'error',
		"message": "> Error: Joining server failed. The user's port number is already used."
		}
		return error
	# If port address is available, add to users
	addresses.append(address)
	success = {
		"command": 'join',
		"message": '> Connection to the Message Board Server is successful!'
	}
	print('A new user ', address, ' has connected to the server.')
	return success


#Register user if user has not yet registered a name and return appropriate response to the client
def register_user(request, address):

	if not isConnected(address):
		error = {
			"command": 'error',
			"message": "> Error: Registration failed. Port number is not connected to server."
		}
		return error

	# Also prevents repeated registering
	elif isRegistered(request['handle'], address):
		error = {
			"command": 'error',
			"message": '> Error: Registration failed. Handle or alias already exists.'
		}
		
		return error

	else:
		registered_users.append({ "username": request['handle'], "address": address})
		success = {
			"command": 'success',
			"message": '> Registration successful. Welcome, ' + request['handle'] + '!'
		}

		print('Current list of registered users: ', registered_users)
		return success


# Stores all sent messages into a queue
def receiveMessages():
	while True:
		try:
			msg, adr = server.recvfrom(1024)

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


			if message['command'] == "join":
				res = join_user(address)

				json_response = json.dumps(res).encode('utf-8')

				server.sendto(json_response, address)
				
			elif message['command'] == "register":
				#process registration, results are in the form of a dict
				res = register_user(message, address)

				#convert dictionary to JSON (for interpoability), encode into bytes
				json_response = json.dumps(res).encode('utf-8')
			
				server.sendto(json_response, address)

			elif message['command'] == "all":
				pass

			elif message['command'] == "msg":
				pass

			elif message['command'] == "leave":
				pass


#Check if an address is already connected
def isConnected(address):
	ip, port = address
	for adr in addresses:
		if adr == address or udp_port == port:
			return True
	
	return False


# Check if user is already registered or username is taken
def isRegistered(username, address):
	for user in registered_users:
		if user['username'] == username or user['address'] == address:
			return True

	return False

			
receiving_thread = threading.Thread(target=receiveMessages)
broadcast_thread = threading.Thread(target=broadcastMessages)

receiving_thread.start()
broadcast_thread.start()