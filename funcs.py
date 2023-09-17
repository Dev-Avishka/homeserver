import os

def buyapple(self):
    print("bought apple")
    self.socket.send(b"apple")
