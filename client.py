

import socket
import json
import sys
import threading

def display_commands():
    print('---------------------------------------------------------------------------')
    print('Welcome to message board app! Please be informed of the following commands:')
    print('/join <server_ip_add> <port>')
    print('/leave')
    print('/register <handle>')
    print('/all <message>')
    print('/msg <handle> <message>')
    print('/?')
    print('----------------------------------------------------------------------------')


def register_user(client_handle):
  
    #dictionary to convert to JSON
    register = {
        "command" : "register", 
        "handle" :  client_handle
    }

    return register

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # For UDP

udp_host = "127.0.0.1"		# Host IP
udp_port = 12345


run_client = True
# specified port to connect
print ("UDP target IP:", udp_host)
print ("UDP target Port:", udp_port)
display_commands()

def listen():
    while True:
        try:
            data, server_addr = sock.recvfrom(1024)

            server_response = json.loads(data)

            print(server_response['message'], "\n")
        except Exception as e:
            pass

def send():
    while True:
        input_script = input()

        slash = input_script[0]

        if(slash == '/' and len(input_script) > 1):
            
            splitted_script = input_script[1:].split(sep=' ')

            if splitted_script[0] == "join" and len(splitted_script) == 3:
                msg = {
                    "command": "join",
                    "message": splitted_script[1:]
                }
                jsonRequest = json.dumps(msg)

                try:
                    sock.sendto(bytes(jsonRequest, 'utf-8'), (udp_host, udp_port))
                except Exception as e:
                    print(e)


            elif splitted_script[0] == 'register':
                try:
                    request_to_register = register_user(splitted_script[1])
                    jsonRequest = json.dumps(request_to_register)

                    try:
                        sock.sendto(bytes(jsonRequest, 'utf-8'),(udp_host,udp_port))
                    except Exception as e:
                        print("Error: ", e)

                except Exception as e:
                    print(e)


            elif splitted_script[0] == 'all':
                msg = {
                    "command": "all",
                    "message": " ".join(splitted_script[1:])
                }
                jsonRequest = json.dumps(msg)
                try:
                    sock.sendto(bytes(jsonRequest, 'utf-8'), (udp_host, udp_port))
                except Exception as e:
                    print(e)


            elif splitted_script[0] == 'msg' and len(splitted_script) >= 3:
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


            elif splitted_script[0] == 'leave':
                run_client = False


            elif splitted_script[0] == '?':
                display_commands()
                pass

        else:
            print("Please Enter Valid Command\n")

t1 = threading.Thread(target=listen)
t1.start()

t2 = threading.Thread(target=send)
t2.start()
   
# x = ["ye","test","yeye","hello","hi"]
# print(" ".join(x[1:]))



 

    



    





    
    		