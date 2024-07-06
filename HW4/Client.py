# By:
# Kobi Alen - 318550985
# Matan Kahlon - 316550458
import socket
import threading
import struct
import time
ports = [1010, 1020, 1030, 1040, 1050]
serversForTimeCheck = []
chosenPort = ports[int(input("Pick a port number(0-4): "))]
clientName = input("What's your name? ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(('127.0.0.1', chosenPort))

server_list_received = threading.Event()

def clientRegister(connSock, name,connPort):
    try:
        header = struct.pack('>bbhh', 2, 1, len(name), 0)
        connSock.send(header)
        connSock.send(name.encode())
        print("connected successfully to:", connPort)
        print("asking my server for list.")
        serverAsk = struct.pack('>bbhh', 5, 0, 0, 0)
        connSock.send(serverAsk)
    except Exception as e:
        print("bye")

def waitForMsg(sock):
    try:
        global serversForTimeCheck
        while True:
            incomingHeader = sock.recv(6)
            type, subtype, length, sublen = struct.unpack('>bbhh', incomingHeader)
            if type == 3:
                sender, rest = sock.recv(length).decode().split('\0')
                receiver, text = rest.split(' ', 1)
                print(sender + ": " + text)
            if type == 5:
                serversList = sock.recv(length).decode().split('\0')
                serversList.append(str(chosenPort))
                serversList = [int(num) for num in serversList if num]  # Remove empty strings
                print("Server list received.")
                serversForTimeCheck = serversList
                server_list_received.set()
    except Exception as e:
        print("bye")

def checkTimeDiff(portList,sock):
    try:#test try
        print("Checking the connection time for each server.")
        rttResults={}
        # minrtt=100000
        for server in portList:
            #there was try here
            tempSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            
            tempSock.connect(('127.0.0.1', server))
            startTime=time.time()
            ping = struct.pack('>bbhh',5,1,0,0)
            tempSock.send(ping)
            pong=tempSock.recv(4).decode()
            print(pong)
            endTime=time.time()
            rtt=endTime-startTime
            rttResults[server]=rtt
            # if rtt<=minrtt:
            #     rttResults[0]=server
            tempSock.close()
        print(rttResults)
        minrtt=min(rttResults, key=rttResults.get)
        print("the server with min rtt is: ",minrtt)
        remove=struct.pack('>bbhh',5,2,0,0)
        sock.send(remove)
        sock.send(clientName.encode())
        sock.close()
        finalSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        finalSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        finalSock.connect(('127.0.0.1', minrtt))
        clientRegister(finalSock,clientName,minrtt)
    except Exception as e:
        print("bye")


# Registering the client
# header = struct.pack('>bbhh', 2, 1, len(clientName), 0)
# sock.send(header)
# sock.send(clientName.encode())
# print("Connected successfully to:",chosenPort,".")
# print("Asking my server for list.")
# serverAsk = struct.pack('>bbhh', 5, 0, 0, 0)
# sock.send(serverAsk)

clientRegister(sock,clientName,chosenPort)
thread = threading.Thread(target=waitForMsg, args=(sock,))
thread.start()

print("Waiting for server list...")
server_list_received.wait()

checkTimeDiff(serversForTimeCheck,sock)
# print(serversForTimeCheck)

while True:
    message = input()
    header = struct.pack('>bbhh', 3, 0, len(clientName) + len(message), len(clientName))
    sock.send(header)
    sock.send(message.encode())
