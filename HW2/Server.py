import socket
import threading

#connections = {}
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


def waitForAccept():
    for port in ports:
        if port is not chosenPort:
            try:
                tempsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                tempsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                tempsock.connect(('127.0.0.1', port))
                print(f'connection successful to port: {port}')
                tempsock.send(b'Hello')
                data = tempsock.recv(1024)
                print(f'Received from port {port}: {data.decode()}')
            except ConnectionRefusedError:
                print(f'Connection failed to port: {port}')


threading.Thread(target=waitForAccept(), args=()).start()

while True:
    conn, client_address = sock.accept()
    print('New connection from', client_address)
    threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
 
