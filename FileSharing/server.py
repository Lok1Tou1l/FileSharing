import os
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFileDialog, QPushButton

class FileServer:
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
