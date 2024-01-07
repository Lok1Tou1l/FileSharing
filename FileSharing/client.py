import socket

class client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_file_list(self, file_list):
        self.sock.sendall(file_list.encode())
    
    def send_file(self, filename):
        with open(filename, 'rb') as file:
            self.sock.sendall(file.read())

    def receive_file(self, filename):
        with open(filename, 'wb') as file:
            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                file.write(data)

    def close_connection(self, data):
        self.sock.sendall(data.encode())
        self.sock.close()

    def receive_file_list(self,file_list):
        file_list = self.sock.recv(1024)
        return file_list.decode('utf-8')


