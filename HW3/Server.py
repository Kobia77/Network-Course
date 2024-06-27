import socket
import threading
import struct

serversDict = {}
clientsDict = {}
ports = [1010, 1020, 1030, 1040, 1050]
chosenPort = ports[int(input("Pick a port number(0-4): "))]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', chosenPort))
sock.listen(1)


def respond_to_client(conn_socket, client_address):
    data = conn_socket.recv(1024)
    



    print(f'Recieved {data.decode()} from {client_address}')
    conn_socket.send(b'World\nEND')



def actAsClient():
    for port in ports:
        if port is not chosenPort:
            try:
                tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                tempsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                tempsock.connect(('127.0.0.1', port))
                serversDict[port]=tempsock
                #print(f'connection successful to port: {port}')
                data = struct.pack('>bbhh',0,0,0,0)
                tempsock.send(data)
                firstRecieved = tempsock.recv(6)
                type,subtype,length,sublen=struct.unpack('>bbhh',firstRecieved)
                secondRecieved = tempsock.recv(length)
                #something with the recv HERE
            except ConnectionRefusedError:
                print(f'Connection failed to port: {port}')


threading.Thread(target=actAsClient(), args=()).start()

while True:
    conn, client_address = sock.accept()
    print('New connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
 
