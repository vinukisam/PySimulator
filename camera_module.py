import socket
import threading
import keyboard
import requests
import json

#Port
IMG_PORT = 12123
CONVEYOR_PORT = 12121

class Listener:
    def __init__(self):
        self.stop_event = threading.Event()

    # Function to handle incoming socket connections
    def handle_client(self, client_socket):
        while not self.stop_event.is_set():
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if str(message).startswith("FILE>"):
                    filePath = str(message)[5:]
                    print("Img path:", filePath)
                    self.send_file_to_api(filePath)                    
            except:
                break

    def send_file_to_api(self, filePath):
        url = 'https://cookietest-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/b690e8e3-f829-4219-98bf-f8b00f79abb3/detect/iterations/Iteration1/image'
        headers = {
            'Prediction-Key': '83cbb48fe107400c818014b9c892e08b',
            'Content-Type': 'application/octet-stream'
        }
        with open(filePath, 'rb') as file:
            response = requests.post(url, headers=headers, data=file)

        print(response.status_code)
        data = json.loads(response.text)

        #find any Bad cookie with prediction rate more than 0.8
        filtered_predictions = [
            prediction for prediction in data["predictions"]
            if prediction["probability"] > 0.8 and prediction["tagName"] == "Bad"
        ]
        badCount = len(filtered_predictions)
        print(f"Bad cookies in {filePath}: {badCount}")
        if badCount>0:
            self.activate_arm()

    
    # Start a thread to handle incoming connections
    def start_server(self, server):
        while not self.stop_event.is_set():
            try:
                client_socket, addr = server.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.daemon = True
                client_handler.start()
            except:
                break

    def start_listening(self):
        # Set up the socket server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', IMG_PORT))
        server.listen(5)
        # Create a stop event
        server_thread = threading.Thread(target=self.start_server, args=(server,))
        server_thread.daemon = True
        server_thread.start()
    
    def activate_arm(self):
        # Connect to the Pygame application
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', CONVEYOR_PORT))

        # Send a message to trigger a Pygame event
        client.send('PUSH'.encode('utf-8'))
        client.close()
#-------------------------------------------------------------------------------------




listen = Listener()
listen.start_listening()
print("Press 'Esc' to exit the application.")

while True:
    # Check if the Escape key is pressed
    if keyboard.is_pressed('esc'):
        print("Escape key pressed. Exiting...")
        break