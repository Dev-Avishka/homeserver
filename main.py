import socket
import threading
import subprocess

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, id, name):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def run(self):
        while True:
            try:
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    print("Client " + str(self.address) + " has disconnected")
                    connections.remove(self)
                    self.socket.close()
                    break
                print("ID " + str(self.id) + ": " + data)
                # Execute the system command and capture the output
                try:
                    output = subprocess.check_output(data, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                    self.socket.send(output.encode("utf-8"))
                except subprocess.CalledProcessError as e:
                    error_message = "Error: " + str(e.returncode) + "\n" + e.output
                    self.socket.send(error_message.encode("utf-8"))

            except Exception as e:
                print("Error handling client:", e)
                break

def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name"))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()

if __name__ == "__main__":
    main()
