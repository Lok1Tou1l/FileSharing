import os
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFileDialog, QPushButton

class FileServer:
    port = 8080
    address = 'localhost'
    
    def __init__(self, directory, address, port):
        self.directory = directory
        self.address = address
        self.port = port

    def get_file_list(self):
        file_list = os.listdir(self.directory)
        return file_list

    def send_file_list(self, file_list):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.address, self.port))
        server_socket.listen(5)

        while True:
            client_socket, _ = server_socket.accept()
            client_socket.sendall(str(file_list).encode())
            client_socket.close()

    def start_server(self):
        print(f"Server started at {self.address}:{self.port}")
        file_list = self.get_file_list()
        self.send_file_list(file_list)
    
    def discover_servers():
        broadcast_address = '<broadcast>'
        broadcast_port = 8080

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client_socket.settimeout(5)

        client_socket.sendto(b"DISCOVER", (broadcast_address, broadcast_port))

        try:
            while True:
                data, server_address = client_socket.recvfrom(1024)
                print(f"Discovered server at {server_address[0]}:{server_address[1]}")
        except socket.timeout:
            pass

        client_socket.close()
