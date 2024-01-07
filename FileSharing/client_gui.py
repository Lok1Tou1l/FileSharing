from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from client import client
import sys

class ClientThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.client = client('192.168.1.39', 8080)  # replace with your host and port

    def run(self):
        files = self.client.receive_file_list()
        self.signal.emit(files)

class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.client_thread = ClientThread() 
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Client')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.data_widget = QTextEdit()
        self.data_widget.setReadOnly(True)
        self.layout.addWidget(self.data_widget)

        self.received_file_widget = QTextEdit()
        self.received_file_widget.setReadOnly(True)
        self.layout.addWidget(self.received_file_widget)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.start_client)
        self.layout.addWidget(self.connect_button)

        self.receive_file_list_button = QPushButton('Receive File List')
        self.receive_file_list_button.clicked.connect(self.receive_file_list)
        self.layout.addWidget(self.receive_file_list_button)


    def start_client(self):
        message = 'Connected to: ' + self.client_thread.client.host + ':' + str(self.client_thread.client.port)
        self.client_thread = ClientThread()
        self.client_thread.finished.connect(self.client_thread.deleteLater)
        self.client_thread.start()
        self.data_widget.append(message)
        self.client_thread.signal.connect(self.update_data)
        if self.client_thread.isRunning():
            self.connect_button.setEnabled(False)
        
    
    def receive_file_list(self, file_list):
        self.client_thread.client.receive_file_list(file_list)
        file_list = self.receive_file_list(file_list)
        file_list = str(file_list)
        print("file list received")
    
   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientGUI()
    ex.show()
    sys.exit(app.exec_())
