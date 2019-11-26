import socket
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 10000))
try:
    message = "Hello from client"
    client.sendall(message.encode('ascii'))
 
    amount_received = 0
    amount_expected = len(message)
 
    while amount_received < amount_expected:
        data = client.recv(1024)
        amount_received += len(data)
        print ("Response from server:", data)
        break
finally:
    print ("Closing socket")
    client.close()