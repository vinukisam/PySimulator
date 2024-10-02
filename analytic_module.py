import socket
import threading
import cloud_modules
import edge_modules

#Port
IMG_PORT = 12123
CONVEYOR_PORT = 12121

class Listener:
    def __init__(self, isCloud):
        self.stop_event = threading.Event()
        self.isCloud = isCloud

    # Function to handle incoming socket connections
    def handle_analytic_client(self, client_socket):
        #while not self.stop_event.is_set():
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if str(message).startswith("FILE>"):
                filePath = str(message)[5:]
                badCount = 0
                if self.isCloud:
                    module = cloud_modules.CloudAnalyzer()
                    badCount = module.analyzeImage(filePath)
                else:
                    module = edge_modules.EdgeAnalyzer()
                    badCount = module.analyzeImage(filePath)
                
                if badCount>0:
                    self.activate_arm()
        except:
            pass
        client_socket.close()
    
    # Start a thread to handle incoming connections
    def start_analytic_server(self, server):
        while not self.stop_event.is_set():
            try:
                client_socket, addr = server.accept()
                client_handler = threading.Thread(target=self.handle_analytic_client, args=(client_socket,))
                client_handler.daemon = True
                client_handler.start()
            except:
                break

    def start(self):
        print("Starting Analytics Server...")
        # Set up the socket server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', IMG_PORT))
        server.listen(5)
        # Create a stop event
        server_thread = threading.Thread(target=self.start_analytic_server, args=(server,))
        server_thread.daemon = True
        server_thread.start()
    
    def activate_arm(self):
        # Connect to the Pygame application
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', CONVEYOR_PORT))

        # Send a message to trigger a Pygame event
        client.send("PUSH".encode('utf-8'))
        client.close()
#-------------------------------------------------------------------------------------