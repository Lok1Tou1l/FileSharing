import unittest
from unittest.mock import patch
from client import Client

class TestClient(unittest.TestCase):
    def setUp(self):
        self.url = "http://loki.com"
        self.directory = "C://Users//Administrator//Documents//Projects//FileSharing//FileSharing//test"
        self.urlfile = "C://Users//Administrator//Documents//Projects//FileSharing//FileSharing//test//urls.txt"
        self.client = Client(self.url, self.directory, self.urlfile)

    def test_fetch_existing_file(self):
        with patch('client.ServerProxy') as mock_server_proxy:
            mock_server = mock_server_proxy.return_value
            self.client.do_fetch("file.txt")
            mock_server.fetch.assert_called_with("file.txt", self.client.secret)

    def test_fetch_non_existing_file(self):
        with patch('client.ServerProxy') as mock_server_proxy:
            mock_server = mock_server_proxy.return_value
            mock_server.fetch.side_effect = Exception("File not found")
            with patch('builtins.print') as mock_print:
                self.client.do_fetch("non_existing_file.txt")
                mock_print.assert_called_with("Couldn't find the file", "non_existing_file.txt")

    def test_exit(self):
        with patch('sys.exit') as mock_exit:
            self.client.do_exit("")
            mock_exit.assert_called_once()

if __name__ == '__main__':
    unittest.main()