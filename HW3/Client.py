#By:
#Kobi Alen - 318550985
#Matan Kahlon - 316550458

import socket
import threading
import struct

ports = [1010, 1020, 1030, 1040, 1050]
chosenPort = ports[int(input("Pick a port number(0-4): "))]
clientName= input("What's your name? ")

sock = socket.socket (socket.AF_INET, socket. SOCK_STREAM, 0) 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(('127.0.0.1', chosenPort)) 
print('successful connection')

#registering the client
header=struct.pack('bbhh',2,1,len(clientName),0)
sock.send(header)
sock.send(clientName.encode())

def waitForMsg(sock):
    while True:
        incomingHeader = sock.recv(6)
        type,subtype,length,sublen = struct.unpack('>bbhh',incomingHeader)
        if type==3:
            sender,rest = sock.recv(length).decode().split('\0')
            receiver,text=rest.split(' ',1)
            print(sender+": "+text)

threading.Thread(target=waitForMsg,args=(sock,)).start()

while True:
    
    message = input()
    header=struct.pack('>bbhh',3,0,len(clientName)+len(message),len(clientName))
    sock.send(header)
    sock.send(message.encode())



    
    


  