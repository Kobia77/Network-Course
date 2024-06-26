import socket

UDP_IP = '0.0.0.0'
UDP_PORT = 9999
clientsAddress = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((UDP_IP, UDP_PORT))

def get_keys_by_value(d, target_value):
    keys = [key for key, value in d.items() if value == target_value]
    return keys

while True:
    data, addr = sock.recvfrom(1024)

    if addr not in clientsAddress.values():
        clientsAddress[data.decode()] = addr
        sender = "".join(get_keys_by_value(clientsAddress, addr))
        print(sender)
        print(clientsAddress)
    else:
        receiver, message = data.decode().split(maxsplit=1)
        if receiver in clientsAddress.keys():
            sender ="".join(get_keys_by_value(clientsAddress, addr))
            nMessage=sender+": "+message
            sock.sendto(nMessage.encode(), clientsAddress[receiver])
        else:
            sock.sendto("The user doesn't exists".encode(), addr)






