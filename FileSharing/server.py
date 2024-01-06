import os 
import socket
import threading

class server:
    def __init__(self, host, port):
        self.host = host 
        self.port = port 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.running = False

    def start(self):
        self.sock.listen(5)
        self.running = True
        while self.running:
            client, adress = self.sock.accept() 
            print(f"Client connected {adress[0]} port : {adress[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()

    def handle_client(self, client):
        while True:
            message = client.recv(1024).decode()
            if message:
                print(f"Received message from client: {message}")
                if message == "send":
                    file_path = client.recv(1024).decode()
                    self.send_file(client, file_path)
                else:
                    client.send(message.encode())
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
    

    
    def send_data(self, data):
        self.sock.send(data.encode())

    def stop(self):
        self.running = False
        self.sock.close()
    
    def send_file_list(self):
        file_list = os.listdir()
        self.sock.send(str(file_list).encode())



    

   
    
    