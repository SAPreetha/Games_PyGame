import pygame
import socket
import json
import threading
import queue

class Player():
    def __init__(self, center, color):
        self.center = center
        self.color = color
        self.size = 10
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.size)

    def set_pos(self, center):
        self.center = center

class Game():
    def __init__(self):
        pygame.init()
        # drawing window
        self.screen = pygame.display.set_mode([500, 500])
        self.running = True
        self.player_1 = Player((100,100),(255,0,0))
        self.player_2 = Player((200,200),(0,0,255))
        self.network_mode = False

    def quit(self):
        pygame.quit()

    def sock_recv(self, s, p2):
        while True:
            try:
                R_data = s.recv(10)
                R_data = R_data.decode("utf-8")
                R_data = json.loads(R_data)
                p2.set_pos(R_data)
            except:
                continue
    def connect(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.t=threading.Thread(target = self.sock_recv, args = (self.sock, self.player_2))
        self.t.start()

    def disconnect(self):
        self.t.join()
        self.sock.close()

    def host(self, port):
        hostname = self.detect_host()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(hostname, port)
        self.sock.bind((hostname, port))
        self.sock.listen(5)
        self.c, addr = self.sock.accept()
        print("hi")
        self.sock = self.c
        self.t = threading.Thread(target=self.sock_recv, args=(self.sock, self.player_2))
        self.t.start()

    def detect_host(self):
        temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp.connect(("192.168.0.1",100))
        hostname = temp.getsockname()[0]
        temp.close()

        return hostname

    def run(self):
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.event_handler(event)

            self.display(self.player_1, self.player_2)

        self.quit()
    def event_handler(self, event):

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                center = pygame.mouse.get_pos()
                self.player_1.set_pos(center)
                if self.network_mode == True:
                    S_data = json.dumps(center)
                    self.sock.send(bytes(S_data, encoding="utf-8"))


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.host(12343)
                self.network_mode = True
            if event.key == pygame.K_c:
                self.connect("192.168.0.103",12343)
                self.network_mode = True


    def display(self, p1, p2):
        self.screen.fill((255, 255, 255))
        p1.draw(self.screen)
        p2.draw(self.screen)

        # pygame.draw.rect(self.screen, (255, 255, 0), (0, 490, 500, 500))
        # pygame.draw.rect(self.screen, (255, 255, 0), (0, 0, 500, 10))
        # pygame.draw.rect(self.screen, (255, 255, 0), (0, 0, 10, 500))
        # pygame.draw.rect(self.screen, (255, 255, 0), (490, 0, 500, 500))

        pygame.display.flip()



        # boundary




class background():
    # if you have  complex background that runs irrespective of the game players
    pass





def main():
    G = Game()
    G.run()

if __name__ == "__main__":
    main()