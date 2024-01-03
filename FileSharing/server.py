import os 
import socket
import threading


class server:
    def __init__(self, host, port):
        self.host = host 
        self.port = port 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    
    def start(self):
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client, address = self.sock.accept()
            print(f"New connection from {address[0]}:{address[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

    def handle_client(self, client):
        while True:
            message = client.recv(1024).decode()
            if message:
                print(f"Received message from client: {message}")
                if message == "send_file":
                    self.send_file(client, "path/to/file.txt")  # Replace with the actual file path
            else:
                break

    def send_file(self, client, file_path):
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                data = file.read(1024)
                while data:
                    client.send(data)
                    data = file.read(1024)
            print("File sent successfully")
        else:
            print("File not found")



if __name__ == "__main__":
    server = server('192.168.1.39', 8000)
    server.start()
    

   
    
    