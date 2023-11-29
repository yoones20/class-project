from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWebSockets import QWebSocket

class ChatWindow(QMainWindow):
    def init(self, parent=None):
        super().init(parent)

        self.websocket = QWebSocket()

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)

        self.chat_display = QTextBrowser(self)
        self.layout.addWidget(self.chat_display)

        self.input_box = QLineEdit(self)
        self.layout.addWidget(self.input_box)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setCentralWidget(self.central_widget)

        self.websocket.connected.connect(self.websocket_connected)
        self.websocket.textMessageReceived.connect(self.message_received)

        self.websocket.open(QUrl("ws://127.0.0.1:8000/ws/1"))  # اطمینان حاصل کنید که client_id مناسب باشد

    def websocket_connected(self):
        print("Connected to WebSocket")

    def message_received(self, message):
        self.chat_display.append(message)

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.websocket.sendTextMessage(message)
            self.input_box.clear()

if __name__ == "main":
    app = QApplication([])
    window = ChatWindow()
    window.show()
    app.exec()