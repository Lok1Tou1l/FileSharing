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
        data = self.client.receive_data()
        self.signal.emit(data)

class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Client')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.data_widget = QTextEdit()
        self.data_widget.setReadOnly(True)
        self.layout.addWidget(self.data_widget)

        self.input_line = QLineEdit()
        self.layout.addWidget(self.input_line)

        self.send_button = QPushButton('Send Data')
        self.send_button.clicked.connect(self.send_data)
        self.layout.addWidget(self.send_button)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.start_client)
        self.layout.addWidget(self.connect_button)

    def send_data(self):
        data = self.input_line.text()
        self.client_thread.client.send_data(data)
        self.input_line.clear()

    def start_client(self):
        self.client_thread = ClientThread()
        self.client_thread.signal.connect(self.update_data)
        self.client_thread.start()

    def update_data(self, data):
        client.receive_data(data)
        self.data_widget.append(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClientGUI()
    ex.show()
    sys.exit(app.exec_())
