from socket import socket
from PySide2.QtWidget import QWidget
from views.chat import ChartForm 
import socket 
import threading


class ChatWindows(QWidget, ChatForm):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUI(self)

        self.connect()
        self.sendButton.clicked.connect(self.send_messages)

    def connect(self):
        connection_data = ("127.0.0.1, 55555")
        af_inet = socket.AF_INET
        sock_stream = socket.SOCk_STREAM
        
        self.client = socket.socket(af_inet, sock_stream)
        self.client.connect(connection_data)

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.deamon = True 
        receive_thread.start()

        self.client.send(self.username.encode("utf-8"))
    
    def receive_messages(self):
        while True:
            try: 
                message = self.client.recv(1024).decode("utf-8")
                self.chatTextEdit.append(message)
            except: 
                self.client.close()
    
    def send_messages(self):
        message = self.messageLineEdit.text()

        message = f"{self.username}: {message}"
        self.client.send(message.encode("utf-8"))
        self.chatTextEdit.append(message)
        self.messageLineEdit.clear()
