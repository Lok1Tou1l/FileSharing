import server 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class FileSharingApp(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])
        
        # Create a main window
        self.window = QtWidgets.QWidget()

        # Create layout for the main window
        self.layout = QtWidgets.QVBoxLayout()

        # Create a file dialog for selecting the directory
        self.file_dialog = QtWidgets.QFileDialog()
        self.file_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        self.layout.addWidget(self.file_dialog)

        # Create a button to trigger sending the file list
        self.button_send_file_list = QtWidgets.QPushButton("Send File List")
        self.button_send_file_list.clicked.connect(self.send_file_list_clicked)
        self.layout.addWidget(self.button_send_file_list)

        # Create a button to start the server
        self.button_start_server = QtWidgets.QPushButton("Start Server")
        self.button_start_server.clicked.connect(self.start_server)
        self.layout.addWidget(self.button_start_server)

        # Set the layout for the main window
        self.window.setLayout(self.layout)

        # Show the main window
        self.window.show()

        self.setStyleSheet("""
            QWidget {
                background-color: #333333;
                color: #ffffff;
            }
            
            QLineEdit, QTextEdit {
                background-color: #555555;
                color: #ffffff;
                border: 1px solid #ffffff;
            }
            
            QPushButton {
                background-color: #555555;
                color: #blue;
                border: 1px solid #ffffff;
                padding: 5px;
            }
            
            QComboBox {
                background-color: #555555;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 5px;
            }
        """)

    def send_file_list_clicked(self):
        # Get the selected directory from the file dialog
        directory = self.file_dialog.directory().absolutePath()

        # Get the list of files in the directory
        file_list = server.get_file_list(directory)

        # Send the file list to connected clients
        server.send_file_list(file_list)

    def start_server(self):
        # Start the server
        server.start_server()

    def run(self):
        # Run the PyQt5 application
        self.exec_()

app = FileSharingApp()
app.run()
