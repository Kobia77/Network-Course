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
stop_event = threading.Event()########

def clientRegister(connSock, name,connPort):
    try:
        header = struct.pack('>bbhh', 2, 1, len(name), 0)
        connSock.send(header)
        connSock.send(name.encode())
        print("connected successfully to:", connPort)
        print("asking my server for list.")
        serverAsk = struct.pack('>bbhh', 5, 0, 0, 0)
        connSock.send(serverAsk)
    except ConnectionAbortedError as e:
        print("closed a connection")
    except Exception as e:
        print("bye")

def finalClientRegister(connSock, name,connPort):
    try:
        header = struct.pack('>bbhh', 2, 1, len(name), 0)
        connSock.send(header)
        connSock.send(name.encode())
        print("connected successfully to:", connPort)
    except ConnectionAbortedError as e:
        print("closed a connection")
    except Exception as e:
        pass


def waitForMsg(sock):
    try:
        global serversForTimeCheck
        while not stop_event.is_set():############
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
    except ConnectionAbortedError as e:
        print("closed a connection")
    except Exception as e:
        pass

def checkTimeDiff(portList,sock):
    try:
        print("Checking the connection time for each server.")
        rttResults={}
        for server in portList:
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
            tempSock.close()
        print(rttResults)
        minrtt=min(rttResults, key=rttResults.get)
        print("the server with min rtt is: ",minrtt)
        return minrtt
    except ConnectionAbortedError as e:
        print("closed a connection")
    except Exception as e:
        pass

clientRegister(sock,clientName,chosenPort)
thread = threading.Thread(target=waitForMsg, args=(sock,))
thread.start()

print("Waiting for server list...")
server_list_received.wait()

minrtt=checkTimeDiff(serversForTimeCheck,sock)
remove=struct.pack('>bbhh',5,2,0,0)
sock.send(remove)
sock.send(clientName.encode())
stop_event.set() ############33 # Signal the thread to stop
thread.join()################     # Wait for the thread to finish
sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect(('127.0.0.1', minrtt))
finalClientRegister(sock,clientName,minrtt)
stop_event.clear()#########
thread = threading.Thread(target=waitForMsg, args=(sock,))
thread.start()
while True:
    message = input()
    header = struct.pack('>bbhh', 3, 0, len(clientName) + len(message), len(clientName))
    sock.send(header)
    sock.send(message.encode())
