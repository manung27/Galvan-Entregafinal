from PySide2.QtWidget import QWidget
from views.login import LoginForm

class LoginWindow(QWidget, LoginForm)
    def __init__(self):
        super().__init__()
        self.setupUI(self)

    def join_to_chat(self):
        username = self.usernameLineEdit.text()

        if username != "":
            from controllers.chat import ChatWindow
            self.chat_window = ChatWindow()
            self.chat_window.show()
            self.close
        else:
            msgboxes.input_error_msgbox("Dato requerido", "Debe introducir un username")

