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
        self.sock.listen(1)
        self.running = True
        while self.running:
            client,address = self.sock.accept() 
            print(f"Client connected {address[0]} port: {address[1]}")
            client_thread = threading.Thread(target=self.handle_client, args=(client,))
            client_thread.start()
        
    def handle_client(self, client):
        while self.running:
            try:
                data = 'client connected'
                if data:
                    print(data.decode('utf-8'))
                    client.send(data)
                else:
                    raise print('Client disconnected')
            except:
                client.close()
                return False
        pass

    def send_file_list(self, file_list):
        file_list = str(os.listdir())
        self.sock.sendall(file_list.encode())

    def stop(self):
        self.running = False
        self.sock.close()
    
    def is_connected(self):
        return self.running
