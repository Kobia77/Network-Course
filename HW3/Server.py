import socket
import threading
import struct

myServerConnections = {}
clients = {}
ports = [1010, 1020, 1030, 1040, 1050]
chosenPort = ports[int(input("Pick a port number(0-4): "))]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', chosenPort))
sock.listen(1)


def getKeysByValue(d, target_value):
    keys = [key for key, value in d.items() if value == target_value]
    return ' '.join(keys)

def respond_to_client(conn_socket, client_address):
    while True:
        print("waiting for recv\n")
        data = conn_socket.recv(6)
        type,subtype,length,sublen = struct.unpack('>bbhh',data)
        print("recv type:",type," subtype: ",subtype)


        if type==0:
            if subtype==0:
                print("ze kobi\n")
                newPort=int(conn_socket.recv(4).decode())
                dualPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)#added two lines here
                dualPort.connect(('127.0.0.1',newPort))
                print(dualPort)
                myServerConnections[newPort]=dualPort
                print(list(myServerConnections.keys()))
                myConnectionsStr=""
                for server in myServerConnections:
                    myConnectionsStr+= '127.0.0.1'+':'+str(server)+"\0"
                outGoingData1 = struct.pack('>bbhh',1,0,len(myConnectionsStr)-1,0)
                conn_socket.send(outGoingData1)
                conn_socket.send(myConnectionsStr.encode())
            if subtype==1:
                pass

        if type==2:
            if subtype==1:
                print("handling new client")
                newClientName=conn_socket.recv(length).decode()
                clients[newClientName]=conn_socket
                print(list(clients.keys()))

        if type==3:

            print("forwarding msg to a client")
            x=conn_socket.recv(length).decode()
            print(x)

            if subtype==0:
                receiver,text=x.split(' ',1)
                sender=getKeysByValue(clients,conn_socket)
                msg = sender+'\0'+receiver+' '+text   
                if receiver not in clients:
                    header=struct.pack('>bbhh',3,1,len(msg),len(sender))
                    broadcast = msg.encode()
                    for server in myServerConnections:
                        if server!=chosenPort:
                            myServerConnections[server].send(header)
                            myServerConnections[server].send(broadcast)          
                else:
                    header=struct.pack('>bbhh',3,0,len(msg),len(sender))
                    print("packed the msg")
                    clients[receiver].send(header)
                    clients[receiver].send(msg.encode())
                    print("sent the msg")

            if subtype==1:
                sender,rest = x.split('\0')
                receiver,text=rest.split(' ',1)
                msg = sender+'\0'+receiver+' '+text 
                if receiver in clients:
                    header=struct.pack('>bbhh',3,0,len(msg),len(sender))
                    print("packed the msg")
                    clients[receiver].send(header)
                    clients[receiver].send(msg.encode())
                    print("sent the msg")
            
        if type==8:
            incomingData = conn_socket.recv(4)
            portForUpdate=int(incomingData.decode())
            print("port for update:\n",portForUpdate,"\n")
            dualPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)#added 2 lines here
            dualPort.connect(('127.0.0.1',portForUpdate))
            myServerConnections[portForUpdate] = dualPort
            print("valuessssssss\n",myServerConnections)
            # print("my dict is: ",list(myServerConnections.keys()))



def splitNewString(longString):
    portsToConnect=longString.split('\0')
    portsToAdd=[]
    for addr in portsToConnect:
        port=addr.split(':')[1]
        portsToAdd.append(port)
    return portsToAdd


def connectToOtherServers(portsList):
    nportsList = [int(num) for num in portsList]
    # newPort = int(conn.recv(4).decode())
    # dualPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # dualPort.connect(('127.0.0.1',newPort))

    for port in nportsList:
        if port!=chosenPort:
            tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            tempsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tempsock.connect(('127.0.0.1', int(port)))
            print("adding port ",port)
            myServerConnections[port]=tempsock
            header = struct.pack('>bbhh',8,0,0,0) # sending my port to who i connected to, for him to add me also to his dict
            tempsock.send(header)
            outGoingData = str(chosenPort).encode()
            tempsock.send(outGoingData)


def actAsClient():
    for port in ports:
        if port is not chosenPort:
            try:
                tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                tempsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                tempsock.connect(('127.0.0.1', port))
                myServerConnections[port]=tempsock
                #print(list(myServerConnections.keys()))
                print("ze rony\n")
                print(myServerConnections)
                infoAsk = struct.pack('>bbhh',0,0,0,0)
                tempsock.send(infoAsk)
                tempsock.send(str(chosenPort).encode())
                print("sent info and chosenport\n")
                firstRecieved = tempsock.recv(6)
                type,subtype,length,sublen=struct.unpack('>bbhh',firstRecieved)
                secondRecieved = tempsock.recv(length)
                secondRecieved=secondRecieved.decode()
                portsToAdd=splitNewString(secondRecieved)#handling the other servers list
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
 
