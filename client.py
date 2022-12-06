

import socket
import json
import sys
import threading

host_ip = socket.gethostbyname(socket.gethostname())	    # Local Host IP Address
server_port = None                                          # Used to check if the client has connected to the server
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # For UDP


def display_commands():
    print('---------------------------------------------------------------------------')
    print('LIST OF COMMANDS:')
    print('/join <server_ip_add> <port> \t - connect to a server')
    print('/leave \t \t \t \t - disconnect from the connected server')
    print('/register <handle> \t \t - register a unique handle for the server')
    print('/all <message> \t \t \t - send a message to everyone in the server')
    print('/msg <handle> <message> \t - send a direct message to a single user')
    print('/? \t \t \t \t - display all input commands')
    print('----------------------------------------------------------------------------')

# --- Dictionary to convert to JSON ---
def join_server():
    join = {
        "command": "join"
    }
    return join

def register_user(client_handle):
    register = {
        "command" : "register", 
        "handle" :  client_handle
    }
    return register


# IDK why but t1.start() causes a runtime error even if you remove the other client.recvfrom(1024)
# def receiveMessages():
#     while True:
#         print('Listening...')
#         try:
#             msg, adr = client.recvfrom(1024)

#             dict_req = json.loads(msg)

#             if dict_req['command'] == "register":
#                 print(dict_req['message'])
#             elif dict_req['command'] == "error":
#                 print(dict_req['message'])
#             else:
#                 print("Unknown Error")

#         except Exception as e:
#             print("Error in receiving messages from server: ", e)
    

# t1 = threading.Thread(target=receiveMessages)
# t1.start()

# Starting Message
print('Welcome to the UDP Message Board! Please be informed of the following commands:')
display_commands()
print('Available server:')
print ("\t Server IP: ", host_ip)
print ("\t Server Port: 12345")
print()

def run():
    while True:
        input_script = input('Enter input script: /')
        splitted_script = input_script.split(sep=' ')

        if splitted_script[0] == 'join' and len(splitted_script) == 3:
            # Try to send a command to the inputted server
            try: 
                join_ip = splitted_script[1]
                join_port = int(splitted_script[2])

                if join_ip != host_ip:
                    raise Exception("Incorrect IP address.")
                else:
                    jsonRequest = json.dumps(join_server())
                    client.sendto(bytes(jsonRequest, 'utf-8'), (host_ip, join_port))
                    
                    msg, adr = client.recvfrom(1024)

                    server_response = json.loads(msg)

                    # If success, update server_port and listen to server
                    if server_response['command'] == 'join':
                        server_port = join_port

                    print(server_response['message'])
                
            except:
                print("> Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")


        elif splitted_script[0] == 'register' and len(splitted_script) == 2:
            
            if server_port == None:
                print("> Error: You need to join a server before you can register.")
            
            else:
                reg_req = register_user(splitted_script[1])

                try:
                    request_to_register = register_user(splitted_script[1])

                    jsonRequest = json.dumps(request_to_register)

                    client.sendto(bytes(jsonRequest, 'utf-8'),(host_ip, server_port))

                    msg, adr = client.recvfrom(1024)

                    server_response = json.loads(msg)

                    print(server_response['message'])

                except:
                    print("Error in register: ", e)

        elif splitted_script[0] == 'all':
            pass
            
        elif splitted_script[0] == 'leave': #WIP
            server_port = None
            print('> Connection closed. Thank you!')
            break

        elif splitted_script[0] == '?':
            display_commands()
        
        else:
            print("> Error: Command not found. Type '/?' to see the list of commands")


t1 = threading.Thread(target=run)
t1.start()

# def send():
#     while True:
#         input_script = input('Enter input script: /')
#         splitted_script = input_script.split(sep=' ')

#         if splitted_script[0] == 'register':

#             reg_req = register_user(splitted_script[1])

#             try:
#                 request_to_register = register_user(splitted_script[1])

#                 #convert dictionary to JSON (for interpoability)
#                 jsonRequest = json.dumps(request_to_register)

#                 # send request to register to server
#                 client.sendto(bytes(jsonRequest, 'utf-8'),(udp_host,12345))

#                 data, server_addr = client.recvfrom(1024)

#                 server_response = json.loads(data)

#                 print(server_response['message'])
#             except Exception as e:
#                 print("Error: ", e)

#         elif splitted_script[0] == 'leave':
#             run_client = False

#         elif splitted_script[0] == '?':
#             display_commands()

# t1 = threading.Thread(target=send)
# t1.start()


   


 

    



    





    
    		