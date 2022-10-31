import json
import socketserver
from pymongo import MongoClient

class MyTCPHandler(socketserver.BaseRequestHandler):
    clients = []

    def handle(self):
        received_data = self.request.recv(2048) #Number of bytes to receive
        if (len(received_data) > 0): #to avoid empty bytes
            split = received_data.split(b'\r\n\r\n', 1)  # seperate headers and body in bytes
            decodedContent = split[0].decode()  # decode headers ONLY
            store = list(decodedContent.split("\r\n"))  # split headers by newlines
            request = str(store[0]).split(" ")  # eg. ['GET', '/style.css', 'HTTP/1.1']
            if(request[1] == "/"):
                opened = open("index.html", 'rb').read()
                length = len(bytes(opened))
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length) + "\r\n\r\n").encode() + opened)
            elif(request[1] == "/style.css"):
                opened = open(request[1][1:], 'rb').read()
                length = len(bytes(opened))
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/css; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length) + "\r\n\r\n").encode() + opened)
            elif(request[1][:8] == "/images/"):
                opened = open(request[1][1:], 'rb').read()
                length = len(bytes(opened))
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/png; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length) + "\r\n\r\n").encode() + opened)
            elif(request[1] == "/teampage.html"):
                opened = open("teampage.html", 'rb').read()
                length = len(bytes(opened))
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(length) + "\r\n\r\n").encode() + opened)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8083

    socketserver.TCPServer.allow_reuse_port = True
    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler) #used to start server
    server.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
