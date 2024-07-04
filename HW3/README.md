# Home Work 3
## Overview
This project consists of a server and a client code for a chat application. Multiple servers can connect and communicate with each other, and clients can connect to these servers to send and receive messages.
The communication is handled using TCP.

## Server Code
The server code handles connections from clients and other servers. It listens on a specified port and can forward messages between clients and other connected servers.

### Features
+ Registers new clients and maintains a list of connected clients.
+ Connects to other servers, exchanges information, and forwards messages between them.

### How to Run the Server
1. Choose a port number from the list: [1010, 1020, 1030, 1040, 1050].
2. Run the server script and input the chosen port number when prompted.
3. The server will listen for incoming connections from clients and other servers.


## Client Code
The client code connects to a specified server, registers the client's name, and allows the client to send and receive messages.

### Features
- Registers the client's name with the server.
- Receives and displays messages from the server.
- Sends messages to other clients via the server(the message template is "receiver text").
### How to Run the Client
1. Choose a port number from the list: [1010, 1020, 1030, 1040, 1050].
2. Run the client script and input the chosen port number when prompted.
3. Input your name when prompted.
4. The client will connect to the server and start sending and receiving messages.



## Authors
- Kobi Alen - 318550985
- Matan Kahlon - 316550458
