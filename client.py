

import socket
import json
import sys

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

udp_host = socket.gethostname()		# Host IP
udp_port = 12345


run_client = True
# specified port to connect
print ("UDP target IP:", udp_host)
print ("UDP target Port:", udp_port)
display_commands()

while run_client == True:
    

    input_script = input('Enter input script: /')
    splitted_script = input_script.split(sep=' ')

    if splitted_script[0] == 'register':
        reg_req = register_user(splitted_script[1])

        try:
            request_to_register = register_user(splitted_script[1])

            #convert dictionary to JSON (for interpoability)
            jsonRequest = json.dumps(request_to_register)
            # send request to register to server
            sock.sendto(bytes(jsonRequest, 'utf-8'),(udp_host,udp_port))
            #wait for response from server
            data, server_addr = sock.recvfrom(1024)

            #convert server response to dict
            server_response = json.loads(data)

                
            print(server_response['message'])
        except:
            print('Uknown error')

        

    elif splitted_script[0] == 'leave':
        run_client = False

    elif splitted_script[0] == '?':
        display_commands()

   


 

    



    





    
    		