import socket
import json
from PyQt5 import QtWidgets

class FileSharingClient:
    def __init__(self):
        self.multicast_group = '224.0.0.1'
        self.server_port = 5000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    def discover_servers(self):
        message = b'Hello, servers!'
        self.sock.sendto(message, (self.multicast_group, self.server_port))

        servers = []
        while True:
            try:
                data, address = self.sock.recvfrom(1024)
                servers.append(address[0])
            except socket.timeout:
                break

        return servers

    def get_shared_files(self, server_address):
        server_port = 5001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, server_port))

        request = {'action': 'list_files'}
        sock.sendall(json.dumps(request).encode())

        response = sock.recv(1024)
        files = json.loads(response.decode())

        sock.close()

        return files

