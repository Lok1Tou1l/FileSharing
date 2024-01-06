from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from server import server
import sys
import time 

host = '192.168.136.93'
port = 8080

class ServerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.server = server(host,port)  # replace with your host and port

    def run(self):
        self.server.start()

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Server')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.data_widget = QTextEdit()
        self.data_widget.setReadOnly(True)
        self.layout.addWidget(self.data_widget)

        self.input_line = QLineEdit()
        self.layout.addWidget(self.input_line)


        self.start_button = QPushButton('Start Server')
        self.start_button.clicked.connect(self.start_server)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Server')
        self.stop_button.clicked.connect(self.stop_server)
        self.layout.addWidget(self.stop_button)
    
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_data)
        self.layout.addWidget(self.send_button)

    def start_server(self):
        message = f"Sever started at {host}:{port}"
        self.data_widget.append(message)
        self.server_thread = ServerThread()
        self.server_thread.start()
    
    def stop_server(self):
        self.server_thread.server.stop()

    def send_data(self):
        data = self.input_line.text()
        self.server_thread.server.send_data(data)
        self.input_line.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerGUI()
    ex.show()
    sys.exit(app.exec_())