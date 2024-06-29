
import socket
import threading
import struct


ports = [1010, 1020, 1030, 1040, 1050]
chosenPort = ports[int(input("Pick a port number(0-4): "))]
clientName= input("What's your name? ")


sock = socket.socket (socket.AF_INET, socket. SOCK_STREAM, 0) 
sock.connect(('127.0.0.1', chosenPort)) 
print('successful connection')

#registering the client
header=struct.pack('bbhh',2,1,len(clientName),0)
sock.send(header)
sock.send(clientName.encode())


while True:
    
    message = input()
    header=struct.pack('>bbhh',3,0,len(clientName)+len(message),len(clientName))#ask about the sublen here!!!
    sock.send(header)
    sock.send(message.encode())



    incomingHeader = sock.recv(6)
    type,subtype,length,sublen = struct.unpack('>bbhh',incomingHeader)
    print("i got msg")
    sender,rest = sock.recv(length).decode().split('\0')
    receiver,text=rest.split(' ',1)
    print(sender+": "+text)


  