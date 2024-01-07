import os 
import socket
import threading

class server:
    def __init__(self, host, port):
        self.host = host 
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = []
        self.running = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"Server started on {self.host}:{self.port}")

        while self.running:
            client_socket, address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"Client connected {address[0]} port: {address[1]}")
            print(f"Number of clients connected: {len(self.client_sockets)}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        if self.running:
            try:
                data = 'client connected'
                if data:
                    print(data.encode('utf-8'))
                    client_socket.send(data.encode())
                else:
                    raise print('Client disconnected')
            except:
                client_socket.close()
                self.client_sockets.remove(client_socket)
                print(f"Number of clients connected: {len(self.client_sockets)}")
                return False

    def send_file_list(self, file_list):
        for client_socket in self.client_sockets:
            client_socket.sendall(file_list.encode())
            print("file list sent")

    def stop(self):
        self.running = False
        for client_socket in self.client_sockets:
            client_socket.close()
        self.server_socket.close()

    def is_running(self):
        return self.running
