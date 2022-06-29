import socket
from threading import Thread
from time import sleep
import datetime

class Log:
    pass

class PTP:
    def __init__(self, , _port: int, _max_clients: int = 1):
        self.running = True
        self.port = _port
        self.max_clients = _max_clients
        self.clients_ip = ["" for i in range(self.max_clients)]
        self.incoming_requests = {}
        self.clients_logs = [Log for i in range(self.max_clients)]
        self.client_sockets = [socket.socket() for i in range(self.max_clients)]
        for i in self.client_sockets:
            i.settimeout(0.2)#TODO


