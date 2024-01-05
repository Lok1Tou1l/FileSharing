from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from server import server
import sys

class ServerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.server = server('192.168.1.39',8080)  # replace with your host and port

    def run(self):
        self.server.start()

class ServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Server GUI')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.start_button = QPushButton('Start Server')
        self.start_button.clicked.connect(self.start_server)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Server')
        self.stop_button.clicked.connect(self.stop_server)
        self.layout.addWidget(self.stop_button)
    
    def start_server(self):
        self.server_thread = ServerThread()
        self.server_thread.start()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerGUI()
    ex.show()
    sys.exit(app.exec_())