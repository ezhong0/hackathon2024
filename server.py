import socket
import threading

host = "127.0.0.1"  # local host
port = 65535  # had to use uncommon number because didn't want to mess with popular ones

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()  # const

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)  # want to sent every client

def handle(client):
    while True:
        try:  # while it works, broadcast message
            message = client.recv(1024)
            broadcast(message)
        except:  #if something fails, it removes the client from the server
            index = clients.index(client)
            clients.remove(clients)
            client.close()
            nickname = nicknames[client]
            broadcast(f"{nickname} left the chat".encode("ascii"))
            nicknames.remove(nickname)
            break

def receive():
    while True:  # server accepting all the clients
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickename of the client is {nickname}')
        broadcast(f"{nickname} joined the chat".encode('ascii'))
        client.send('connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server is listening")
receive()