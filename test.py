import socket

# Connect to the Pygame application
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 11999))

# Send a message to trigger a Pygame event
client.send('KEYDOWN'.encode('utf-8'))
client.close()
