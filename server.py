import socket
import json
import sys
import queue
import threading

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      
udp_host = "127.0.0.1"		        
udp_port = 12345			                

messages = queue.Queue()

print("Server is online.")
print("Running on ", udp_host, " at Port ", udp_port)
print("Waiting for clients...")

# list of registered users
# Registered users are stored as {username: <name>, address: <address>}
registered_users = []
joined_addresses = []

sock.bind((udp_host,udp_port))


# Handle /Register Command
def handleRegister(request, address):
	msg = ""
	if isRegistered(request['handle'], address):
		msg = {
			"command": 'error',
			"message": 'Error: Registration failed, handle or alias already exists'
		}

	else:
		registered_users.append({ "username": request['handle'], "address": address})
		msg = {
			"command": 'success',
			"message": 'Registration successful. Welcome ' + request['handle']
		}
		print('Current list of registered users: ', registered_users[0]['username'])

	json_response = json.dumps(msg).encode('utf-8')
	sock.sendto(json_response, address)


# Handle /Join Command
def handleJoin(message, address):
	ip = message[0]
	port = int(message[1])

	if(udp_host == ip and udp_port == port ):
		msg = "Warning: You are already joined in to Message Board"
		if(address not in joined_addresses):
			joined_addresses.append(address)
			msg = "Connection to the Message Board Server is successful!"
		res = {
			"command": "Success",
			"message": msg
		}
	else:
		res = {
			"command": "Error",
			"message": "Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number."
		}
	
	json_response = json.dumps(res).encode('utf-8')
	sock.sendto(json_response, address)
	print("Address ", address, " has connected")
	

# Handle /All Command
def handleAll(message, address):
	src_user = getUsername(address)
	res = {
		"command": 'all',
		"message": str(src_user) + ": " + message['message']
	}
	json_response = json.dumps(res).encode('utf-8')
	for user in registered_users:
		sock.sendto(json_response, user['address'])


# Handle /Message Command
def handleMsg(message, address, sender):
	
	msg = ""
	receiver_username = message['handle']
	receiver_address = ""

	for user in registered_users:
		if user['username'] == receiver_username:
			receiver_address = user['address']

	print("ADDRESS FOUND: ", receiver_address)
	# If receiver not found
	if len(receiver_address) == 0: 
		res = {
			"command": "msg",
			"message": "Error: Handle or alias not found."
		}
		json_response = json.dumps(res).encode('utf-8')
		sock.sendto(json_response, address)

	else:
		res = {
			"command": "msg",
			"message": "[From " + sender + "]: " + " ".join(message['message'])
		}
		res2 = {
			"command": "msg",
			"message": "[To " + receiver_username + "]: " + " ".join(message['message'])
		}
		json_response = json.dumps(res).encode('utf-8')
		json_response2 = json.dumps(res2).encode('utf-8')
		sock.sendto(json_response, receiver_address)
		sock.sendto(json_response2, address)
	

# Handle /leave Command
def handleLeave(address):
	if address not in joined_addresses:
		res = {
			"command": "error",
			"message": "Error: Disconnection failed. Please connect to the server first."
		}
		json_response = json.dumps(res).encode('utf-8')
		sock.sendto(json_response, address)
		return

	
	for user in registered_users:
		if user['address'] == address:
			registered_users.remove(user)

	joined_addresses.remove(address)

	res = {
		"command": "Success",
		"message": "Connection closed. Thank you!"
	}
	json_response = json.dumps(res).encode('utf-8')
	sock.sendto(json_response, address)


# Send JSON if Not Registered
def notRegistered(message, address):
	if not isRegistered("", address):
		res = {
			"command": 'error',
			"message": 'Error: Please Register first before using this command'
		}
		json_response = json.dumps(res).encode('utf-8')
		sock.sendto(json_response, address)
		return True

	return False


# Send JSON if not Joined
def notJoined(address):
	if address not in joined_addresses:
		res = {
			"command": "error",
			"message": "Error: Please join with valid ip and port"
		}
		json_response = json.dumps(res).encode('utf-8')
		sock.sendto(json_response, address)


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

			# HANDLING JOIN COMMAND
			if message['command'] == "join":
				handleJoin(message['message'], address)
			
			# HANDLING REGISTER COMMAND
			elif message['command'] == "register" and address in joined_addresses:
				handleRegister(message, address)					

			# HANDLING ALL COMMAND
			elif message['command'] == "all" and address in joined_addresses:
				if not notRegistered(message, address):
					handleAll(message, address)

			# HANDLING MSG COMMAND 
			elif message['command'] == "msg" and address in joined_addresses:
				if not notRegistered(message, address):
					handleMsg(message, address, getUsername(address))

			# HANDLING LEAVE COMMAND
			elif message['command'] == "leave":
				handleLeave(address)

			elif address not in joined_addresses:
				notJoined(address)

			else: 
				res = {
					"command": "error",
					"message": "Error: Command not found."
				}
				json_response = json.dumps(res).encode('utf-8')
				sock.sendto(json_response, address)
			

# Check if user is registered
def isRegistered(username, address):
	for user in registered_users:
		if user['username'] == username or user['address'] == address:
			return True

	return False

# Get Username via address
def getUsername(address):
	for user in registered_users:
		if user['address'] == address:
			return user['username']
	return None

# Get address via username
def getAddress(username):
	for user in registered_users:
		if user['username'] == username:
			return user['address']
	return None
			
receiving_thread = threading.Thread(target=receiveMessages)
broadcast_thread = threading.Thread(target=broadcastMessages)

receiving_thread.start()
broadcast_thread.start()