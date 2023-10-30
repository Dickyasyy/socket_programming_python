import socket
import threading

# Inisialisasi server
host = '192.168.1.108'
port = 8888
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = {}

# Fungsi yang akan dijalankan pada setiap thread
def handle_client(client_socket):
    client_name = client_socket.recv(1024).decode()
    clients[client_name] = client_socket

    welcome_message = f"Server : Selamat Datang, {client_name}!"
    client_socket.send(welcome_message.encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                remove_client(client_name)
            else:
                broadcast(message, client_name)
        except:
            continue

def broadcast(message, sender_name):
    for name, client_socket in clients.items():
        if name != sender_name:
            try:
                client_socket.send(f"{sender_name}: {message}".encode())
            except:
                remove_client(name)

def remove_client(client_name):
    if client_name in clients:
        del clients[client_name]

def main():
    print("Server mendengarkan di {}:{}...".format(host, port))

    while True:
        client_socket, client_address = server.accept()
        client_socket.send("Masukkan nama Anda: ".encode())
        client_name = client_socket.recv(1024).decode()

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()

