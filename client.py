

import socket
import json
import sys
import threading
import select

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


def register_user(client_handle):
  
    #dictionary to convert to JSON
    register = {
        "command" : "register", 
        "handle" :  client_handle
    }

    return register

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  
udp_host = "127.0.0.1"		        # Server IP
udp_port = 12345                    # Server Port
sock.settimeout(5)

print('Welcome to the UDP Message Board! Please be informed of the following commands:')
display_commands()
# specified port to connect
print('Available server:')
print ("\t Server IP: ", udp_host)
print ("\t Server Port: ", udp_port)
print()

sock.setblocking(0)

def listen():
    while True:
        try:
            ready = select.select([sock], [], [], 5)
            if ready[0]:
                data, server_addr = sock.recvfrom(1024)
                server_response = json.loads(data)
                print(server_response['message'], "\n")

        except Exception as e:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.\n")

def send():
    has_joined = False                  # To check if the client has joined a server

    while True:

        input_script = input()

        slash = input_script[0]

        if(slash == '/' and len(input_script) > 1):
            
            splitted_script = input_script[1:].split(sep=' ')
            
            if splitted_script[0] == "join":
                if len(splitted_script) == 3:
                    try:
                        join_host = splitted_script[1]
                        join_port = int(splitted_script[2])

                        if join_host != udp_host or join_port != udp_port:
                            raise Exception("Incorrect Server IP Address and/or Server Port.")
                        else:
                            msg = {
                                "command": "join",
                                "message": splitted_script[1:]
                            }
                            jsonRequest = json.dumps(msg)

                            try:
                                sock.sendto(bytes(jsonRequest, 'utf-8'), (udp_host, udp_port))
                                has_joined = True
                            except Exception as e:
                                print("Error in JOIN: ", e)
                    except:
                        print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", "\n")
                else:
                    print("Error: Command parameters do not match or is not allowed. Type '/?' to see the list of commands.", "\n")

            elif splitted_script[0] == 'register':
                if has_joined:
                    if  len(splitted_script) == 2:
                        try:
                            request_to_register = register_user(splitted_script[1])
                            jsonRequest = json.dumps(request_to_register)

                            try:
                                sock.sendto(bytes(jsonRequest, 'utf-8'),(udp_host,udp_port))
                            except Exception as e:
                                print("Error in REGISTER: ", e)

                        except Exception as e:
                            print(e)
                    else:
                        print("Error: Command parameters do not match or is not allowed. Type '/?' to see the list of commands.", "\n")
                else:
                    print("Error: Please connect to the server first before entering other commands.", "\n")


            elif splitted_script[0] == 'all':
                if has_joined:
                    if len(splitted_script) >= 2:
                        msg = {
                            "command": "all",
                            "message": " ".join(splitted_script[1:])
                        }
                        jsonRequest = json.dumps(msg)
                        try:
                            sock.sendto(bytes(jsonRequest, 'utf-8'), (udp_host, udp_port))
                        except Exception as e:
                            print(e)
                    else:
                        print("Error: Command parameters do not match or is not allowed. Type '/?' to see the list of commands.", "\n")
                else:
                    print("Error: Please connect to the server first before entering other commands.", "\n")


            elif splitted_script[0] == 'msg':
                if has_joined:
                    if len(splitted_script) >= 3:
                        msg = {
                            "command": "msg",
                            "handle": splitted_script[1],
                            "message": splitted_script[2:]
                        }
                        jsonRequest = json.dumps(msg)
                        try:
                            sock.sendto(bytes(jsonRequest, 'utf-8'), (udp_host, udp_port))
                        except Exception as e:
                            print(e)
                        print()
                    else:
                        print("Error: Command parameters do not match or is not allowed. Type '/?' to see the list of commands.", "\n")
                else:
                    print("Error: Please connect to the server first before entering other commands.", "\n")


            elif splitted_script[0] == 'leave':
                if has_joined:
                    if len(splitted_script) == 1:
                        msg = {
                            "command": "leave",
                            "message": " ".join(splitted_script[1:])
                        }
                        jsonRequest = json.dumps(msg)
                        try:
                            sock.sendto(bytes(jsonRequest, 'utf-8'), (udp_host, udp_port))
                            has_joined = False
                        except Exception as e:
                            print(e)
                    else:
                        print("Error: Command parameters do not match or is not allowed. Type '/?' to see the list of commands.", "\n")
                else:
                    print("Error: Disconnection failed. Please connect to the server first.", "\n")

            elif splitted_script[0] == '?':
                if len(splitted_script) == 1:
                    display_commands()
                else:
                    print("Error: Command parameters do not match or is not allowed. Type '/?' to see the list of commands.", "\n")
            
            else:
                print("Error: Command Not Found. Type '/?' to see the list of commands.\n")

        else:
            print("Type '/?' to see the list of commands.", "\n")

t1 = threading.Thread(target=listen)
t1.start()

t2 = threading.Thread(target=send)
t2.start()


 

    



    





    
    		