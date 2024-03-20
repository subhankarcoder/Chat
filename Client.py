# Creating every client that wants to join the server
import socket
import threading

# Choosing the nickname for the user
nick = input("Enter your desired Nickname: ")

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',1254))

# Client needs two threads  - one for receiving messages and another for sending them
def recieve():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nick.encode('ascii'))
            else:
                print(message)
        except:
            # Closing the connection in case of error
            print("An error occurred")
            client.close()
            break

def send_message():
    while True:
        message = '{}: {}'.format(nick, input('')).encode('ascii')
        client.send(message)

# Handling two threads
recieve_thread = threading.Thread(target=recieve)
send_thread = threading.Thread(target=send_message)
# Starting both threads
recieve_thread.start()
send_thread.start()