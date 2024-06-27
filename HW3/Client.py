
import socket

sock = socket.socket (socket.AF_INET, socket. SOCK_STREAM, 0) 
sock.connect(('127.0.0.1', 9999)) 


print('successful connection')


while True:
    data = input('Enter line:').strip().encode ()
    sock.send(data)
    reply_data = sock.recv (1024)
    print('server reply:', reply_data.decode())