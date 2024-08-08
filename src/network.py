import socket
import pickle
from env import *
from enemy import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_data(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(BUFSIZE))
        except:
            pass

    def send(self, data):
        out = None
        self.client.send(pickle.dumps(data))
        inp = self.client.recv(BUFSIZE)
        try:
            out = pickle.loads(inp)
            return out
        except:
            # wait until have data
            return self.send(data)
