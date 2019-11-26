# this code for the server part
import socket
import io

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Starting server on port 10000")
server.bind((socket.gethostname(), 10000))
server.listen(1)

while True:
    conn, client = server.accept()
    try:
        print("Connection from", client)

        while True:
            data = conn.recv(1024)
            print("Receive from client:", data.decode('utf-8'))
            if len(data.decode('utf-8')):
                conn.sendall('text'.encode('ascii'))
            else:
                print("No data received")
                break
    finally:
        conn.close()
        break
