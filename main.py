import pygame
import random
import socket
import threading
#from pygame_screen_record import ScreenRecorder

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookie Conveyor Belt Simulation")

class Arm:
    def __init__(self):
        self.width = 100
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - 180
        self.height = 20
        self.color = (120,120,120)
        self.active = False
        self.speed = 0
        self.acceleration = 2
        # Counter for bad cookies and rejected
        self.rejectedCookies = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(screen, self.color, [self.x + (self.width//2 - self.height//2), 
                                              self.y - self.width//2, 
                                              self.height, self.width//2])

    def move(self):
        if self.active:
            self.speed += self.acceleration
            self.y += self.speed
            if self.y > SCREEN_HEIGHT // 2 + 150:  # Move the arm to the right
                self.active = False
                self.speed = 0
                self.y = SCREEN_HEIGHT // 2 - 180  # Reset arm position

    def push(self, cookies):
        if self.active:
            for cookie in cookies:
                if self.x < cookie.x < self.x + self.width and self.y + self.height > cookie.y:
                    cookie.y = self.y  # Push the cookie to the right
                    if cookie.isBad and cookie.dead == False:
                        self.rejectedCookies += 1
                    cookie.dead = True
                    

class Cookie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.dead = False
        self.bad = random.randint(0,10)
        self.isBad = 0<self.bad<4

        if self.bad == 1 or self.bad == 3:
            #self.color = (139,69,19)
            bad_colors = [(40,18,5), (70,20,15), (120,80,80)]
            self.color = bad_colors[random.randint(0,2)]
        else:
            self.color = BROWN

        bad_shape = [(0,0,0), (1,2,5), (3,4,5), (4,5,5)]
        if self.bad == 2 or self.bad ==3:
            self.shape_arc = bad_shape[random.randint(1,3)]
        else:
            self.shape_arc = bad_shape[0]
   
    def draw(self, screen):
        # Draw the full cookie
        pygame.draw.ellipse(screen, 
                            self.color, 
                            [self.x, self.y, self.width, self.height])

        # Draw the bite (an arc)
        pygame.draw.arc(screen,
                        (0,0,0), 
                        [self.x, self.y, self.width, self.height],
                        self.shape_arc[0], self.shape_arc[1], self.shape_arc[2])

    def move(self, speed):
        if(self.dead == False) :
            self.x += speed

class Belt:
    def __init__(self):
        self.color = (0,0,0)
        self.height = 300

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [0, SCREEN_HEIGHT // 2 - self.height//2, SCREEN_WIDTH, self.height])

class Camera:
    def __init__(self):
        self.capture_area = pygame.Rect(SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2 - 150, 68, 300)
        self.cam_poly = [(self.capture_area.left + 10, self.capture_area.top - 10),
                         (self.capture_area.left + 20, self.capture_area.top - 30),
                         (self.capture_area.left + 40, self.capture_area.top - 30),
                         (self.capture_area.left + 50, self.capture_area.top - 10)]

    def draw(self, screen):
        pygame.draw.rect(screen, (200,0,0), self.capture_area, 2)
        pygame.draw.polygon(screen, (100,100,100), self.cam_poly)


def main():
    clock = pygame.time.Clock()
    cookies = []
    speed = 2
    arm = Arm()
    belt = Belt()
    running = True
    stX = 0
    badCookies = 0
    imgCounter = -2

    #-------------------------------------------------------------------------------------
    # Set up the socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 11999))
    server.listen(5)

    # Create a stop event
    stop_event = threading.Event()

    server_thread = threading.Thread(target=start_server, args=(server, stop_event))
    server_thread.daemon = True
    server_thread.start()
    #-------------------------------------------------------------------------------------

    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    # Initialize the screen recorder
    # Capture the defined area
    camera = Camera()
    #capture_surface = screen.subsurface(camera.capture_area)
    #recorder.capture_frame(capture_surface)
    #recorder = ScreenRecorder(60, capture_surface)  # 60 FPS
    #recorder.start_rec()  # Start recording
    
    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_event.set()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                arm.active = True

        # Add a new cookie at random intervals
        if stX == 0:
        #    cookies.append(Cookie(0, SCREEN_HEIGHT // 2 - 25))
            stY = SCREEN_HEIGHT // 2 - (100 + random.randint(0, 45))
            while stY <= SCREEN_HEIGHT // 2 + 100:
                cookie = Cookie(random.randint(0, 10), stY)
                #increment bad cookie counter
                if cookie.isBad:
                    badCookies += 1
                cookies.append(cookie)
                stY += 55

        # Move and draw cookies
        screen.fill(WHITE)
        belt.draw(screen)
        for cookie in cookies:
            cookie.move(speed)
            cookie.draw(screen)

        # Draw and move the arm
        arm.draw(screen)
        arm.move()
        arm.push(cookies)
        
        #Move the X pointer
        stX += speed
        if(stX > 60):
            stX = 0

        # Remove cookies that have moved off the screen
        cookies = [cookie for cookie in cookies if cookie.x < SCREEN_WIDTH]

        # Set up the font
        font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the font size
        text = font.render("Bad Cookies: " + str(badCookies) + " | Rejected Bad Cookies: " + str(arm.rejectedCookies), True, (0,0,0))
        # Blit the text onto the screen
        screen.blit(text, (0, 0))  # Position the text at (100, 100)

        camera.draw(screen)
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        # Capture the defined area
        #capture_surface = screen.subsurface(camera.capture_area)
        #recorder.capture_frame(capture_surface)
        if stX == 0:
            if imgCounter>0:
                capture_surface = screen.subsurface(camera.capture_area)
                capture_image = pygame.Surface(camera.capture_area.size)
                capture_image.blit(capture_surface, (0, 0))
                # Save the captured image
                pygame.image.save(capture_image, f"captured_image{imgCounter}.png")
            imgCounter += 1
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

        pygame.display.flip()
        clock.tick(60)

    try:
        pass
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        #recorder.stop_rec()  # Stop recording
        #recorder.save_recording("partial_recording.mp4")  # Save the recording
        # Capture the defined area
        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    except Exception as e:
        print(f"Error in worker thread: {e}")
        
    pygame.quit()

#-------------------------------------------------------------------------------------
# Function to handle incoming socket connections
def handle_client(client_socket, stop_event):
    while not stop_event.is_set():
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'QUIT':
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif message == 'KEYDOWN':
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
        except:
            break

# Start a thread to handle incoming connections
def start_server(server, stop_event):
    while not stop_event.is_set():
        try:
            client_socket, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, stop_event))
            client_handler.daemon = True
            client_handler.start()
        except:
            break
#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()