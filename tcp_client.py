import socket

target_host = "0.0.0.0"
target_port = 9998

# Create a sockect object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client
client.connect((target_host,target_port))

# Send some data
client.send(b"Hello Aman")

# Receive some data
response = client.recv(4096)

# Display the data
print(response.decode())

# Close the socket object
client.close()
