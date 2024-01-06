from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from server import server
import sys
import os


class ServerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.server = server('192.168.136.93',8080)  # replace with your host and port

    def run(self):
        self.server.start()

class ServerGUI(QWidget):
    file_list = []

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Server')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.file_list_widget = QListWidget()
        self.layout.addWidget(self.file_list_widget)


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
    
        self.choose_file_button = QPushButton('Choose Path')
        self.choose_file_button.clicked.connect(self.choose_directory)
        self.layout.addWidget(self.choose_file_button)

        self.send_file_list_button = QPushButton('Send File List')
        self.send_file_list_button.clicked.connect(self.send_file_list)
        self.layout.addWidget(self.send_file_list_button)

    def start_server(self):
        host = self.input_line.text()
        port = 8080
        message = f"Sever started at {host}:{port}"
        self.data_widget.append(message)
        self.server_thread = ServerThread()
        self.server_thread.start()
    
    def stop_server(self):
        self.server_thread.server.stop()

    
    def send_file_list(self, file_list):
     # Convert the list of file paths to a string
     file_list_str = '\n'.join(file_list)
     # Send the string over the socket
     self.server_thread.server.send_data(file_list_str)

   
    def choose_directory(self):
     dir_path = QFileDialog.getExistingDirectory(self, 'Choose Directory')
     if dir_path:
         file_list = os.listdir(dir_path)
         self.display_file_list(file_list)
         return file_list
    
    def display_file_list(self, file_list):
      self.file_list_widget.clear()
      self.file_list_widget.addItems(file_list)
   
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerGUI()
    ex.show()
    sys.exit(app.exec_())