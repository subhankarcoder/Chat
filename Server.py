# Importing  the required modules
import socket
import threading

# Initializing host and port
HOST = '127.0.0.1'
PORT = 1254

# Starting the server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen() # Waits for clients to connect
print("Server is listening...")

# Creating a list to store Users and their nicknames
clients = []
nicknames = []

# Broadcasting the messages to all users in the chat
def broadcast(message):
    for  client in clients:
        client.send(message)

# Handling messages for  each user individually
def handle_message(client):
    # While user connects to the server perform some task
    while True:
        try:
            # Broadcasting messages
            message = client.recv(1024) # Reciving data upto 1024 bytes
            broadcast(message)
        except: 
            # Removing the client and closing the connection  if any error occurs
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            print(f"{nickname} left the chat")
            nicknames.remove(nickname)
            break

# Recieving Messages from the client
def recieve():
    while True:
        # Getting the user's details
        client, address = server.accept() # Getting  the client information
        print(f"Connected with {address}")

        # When a new client sends a request to the server using the code "NICK", the server will expect a string which is the Nickname of the client
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii') 
        nicknames.append(nickname)
        clients.append(client)

        print("{} joined the chat!".format(nickname).encode('ascii'))
        broadcast("{} joined".format(nickname).encode('ascii'))
        # client.send("Connected to the server...".encode('ascii'))
        # Starting a new thread for handling
        thread = threading.Thread(target=handle_message, args=(client,))
        thread.start()

# Calling the recieve function
recieve()


# End of Server.py

