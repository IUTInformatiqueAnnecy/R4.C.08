import socket

class Server:
    def __init__(self, port):
        # get the hostname
        host = socket.gethostname()
        self.server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind((host, port))  # bind host address and port together
        self.conn = None

    def waitForConnection(self):
        # configure how many client the server can listen simultaneously
        self.server_socket.listen(2)
        self.conn, address = self.server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

    def sendMessage(self, msg: str):
        print("Sending:", msg)
        self.conn.send(str.encode(msg + "@!"))

    def receiveMessage(self):
        msg = self.conn.recv(1024).decode().split("@!")
        return msg

    def sendFile(self, filename: str):
        print("Sending:", filename)
        with open(filename, 'rb') as f:
            raw = f.read()
        # Send actual length ahead of data, with fixed byteorder and size
        self.conn.sendall(len(raw).to_bytes(8, 'big'))
        self.conn.send(raw)  # send data to the client


    def close(self):
        if not self.conn == None:
            self.conn.close()  # close the connection
        else:
            raise Exception("Erreur: la connexion a été fermée avant d'être instanciée.")



if __name__ == '__main__':
    server = Server(5000)
    server.waitForConnection()
    f = "input/test.txt"
    server.sendFile(filename=f)
    server.sendMessage("Ce message a bien été transmis du serveur au client1")
    server.sendMessage("Ce message a bien été transmis du serveur au client2")
    server.sendMessage("Ce message a bien été transmis du serveur au client3")
    server.sendMessage("Ce message a bien été transmis du serveur au client4")
    server.sendMessage("Ce message a bien été transmis du serveur au client5")
    server.close()