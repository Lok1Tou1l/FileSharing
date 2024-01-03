import socket

class client:
    def __init__(self, host, port):
        self.host = host 
        self.port = port 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_data(self, data):
        
        self.sock.sendall(data.encode())

    def receive_data(self):
        received_data = self.sock.recv(1024).decode()
        return received_data

    def close_connection(self,data):
        
        self.sock.sendall(data.encode())
        self.sock.close()


if __name__ == "__main__":
    client = client('192.168.1.39', 8000)
    client.send_data("Hello from client")
    print(client.receive_data())
    client.close_connection("exit")
