from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from server import server
import sys
import os


class ServerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.server = server('192.168.1.39',8080)  # replace with your host and port

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
     self.server_thread = ServerThread()
     self.server_thread.start()
     message = 'Server started at: ' + self.server_thread.server.host + ':' + str(self.server_thread.server.port)
     self.data_widget.append(message)
    
    def stop_server(self):
        self.server_thread.server.stop()

    
    def send_file_list(self):
        try:
            file_list = [item.text() for item in self.file_list_widget.selectedItems()]
            file_list = str(file_list)
            self.server_thread.server.send_file_list(file_list)
            print(file_list)
        except OSError as e:
            self.data_widget.append(f'Error: No client connected{e}')
     

   
    
    def choose_directory(self):
     dir_path = QFileDialog.getExistingDirectory(self, 'Choose Directory')
     if dir_path:
        file_list = os.listdir(dir_path)
        self.display_file_list(file_list)
        return 
    
    def display_file_list(self, file_list):
      self.file_list_widget.clear()
      self.file_list_widget.addItems(file_list)
   
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerGUI()
    ex.show()
    sys.exit(app.exec_())