from PyQt5 import QtWidgets
from client import FileSharingClient

class FileSharingGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = FileSharingClient()
        self.servers = []

        self.setWindowTitle("File Sharing Client")
        self.server_listbox = QtWidgets.QListWidget(self)
        self.server_listbox.setGeometry(10, 10, 200, 200)

        self.discover_button = QtWidgets.QPushButton("Discover Servers", self)
        self.discover_button.setGeometry(10, 220, 200, 30)
        self.discover_button.clicked.connect(self.discover_servers)

    def discover_servers(self):
        self.servers = self.client.discover_servers()
        self.update_server_listbox()

    def update_server_listbox(self):
        self.server_listbox.clear()
        for server in self.servers:
            self.server_listbox.addItem(server)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = FileSharingGUI()
    gui.show()
    app.exec_()
