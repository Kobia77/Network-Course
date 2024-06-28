import socket
import threading
import struct

myServerConnections = {}
clientsDict = {}
ports = [1010, 1020, 1030, 1040, 1050]
chosenPort = ports[int(input("Pick a port number(0-4): "))]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', chosenPort))
sock.listen(1)


def respond_to_client(conn_socket, client_address):
    data = conn_socket.recv(6)
    type,subtype,length,sublen = struct.unpack('>bbhh',data)


    if type==0:
        if subtype==0:
            newPort=int(conn_socket.recv(4).decode())
            myServerConnections[newPort]=conn_socket
            print(list(myServerConnections.keys()))
            
            myConnectionsStr=""
            for server in myServerConnections:
                myConnectionsStr+= '127.0.0.1'+':'+str(server)+"\0"
            outGoingData1 = struct.pack('>bbhh',1,0,len(myConnectionsStr)-1,0)
            conn_socket.send(outGoingData1)
            conn_socket.send(myConnectionsStr.encode())


# 1000:(127.0.0.1,4321)

def splitNewString(longString):
    portsToConnect=longString.split('\0')
    portsToAdd=[]
    for addr in portsToConnect:
        port=addr.split(':')[1]
        portsToAdd.append(port)
    return portsToAdd


def connectToOtherServers(portsList):
    nportsList = [int(num) for num in portsList]
    for port in nportsList:
        print(port," ",chosenPort)
        if port!=chosenPort:
            tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            tempsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tempsock.connect(('127.0.0.1', int(port)))
            print("adding port ",port)
            myServerConnections[port]=tempsock


def actAsClient():
    for port in ports:
        if port is not chosenPort:
            try:
                tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                tempsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                tempsock.connect(('127.0.0.1', port))
                myServerConnections[port]=tempsock
                print(list(myServerConnections.keys()))
                infoAsk = struct.pack('>bbhh',0,0,0,0)
                tempsock.send(infoAsk)
                tempsock.send(str(chosenPort).encode())
                firstRecieved = tempsock.recv(6)
                type,subtype,length,sublen=struct.unpack('>bbhh',firstRecieved)
                secondRecieved = tempsock.recv(length)
                print("second: ",secondRecieved.decode())
                secondRecieved=secondRecieved.decode()
                portsToAdd=splitNewString(secondRecieved)
                connectToOtherServers(portsToAdd)
                print(list(myServerConnections.keys()))

                break
            except ConnectionRefusedError:
                print(f'Connection failed to port: {port}')


#threading.Thread(target=actAsClient(), args=()).start()
actAsClient()


while True:
    conn, client_address = sock.accept()
    print('New connection from', client_address)

    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
 
