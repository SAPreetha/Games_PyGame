import pygame
import socket
import json
import threading
import queue


def data_recv(s,q):
    while True:
        try:
            data = s.recv(10)
            data = json.loads(data.decode('utf-8'))
            q.put(data)
        except:
            continue
pygame.init()

screen = pygame.display.set_mode((500,500))
run = True

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = "192.168.0.101"
PORT = 12345
sock.connect((HOST,PORT))
q = queue.Queue()
t = threading.Thread(target=data_recv, args = (sock,q))
t.start()
center = (250,250)
center2 = (100,100)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed() == (1,0,0):
                center = pygame.mouse.get_pos()
                data = json.dumps(center)
                sock.send(bytes(data,encoding="utf-8"))

    if not q.empty():
        center2 = q.get()
    screen.fill((255,255,255))
    pygame.draw.circle(screen,(0,255,0),center,10)
    pygame.draw.circle(screen,(255,0,0),center2,10)
    pygame.draw.rect(screen,(100,100,0),(0,490,500,500))
    pygame.draw.rect(screen,(100,100,0),(0,0,500,10))
    pygame.draw.rect(screen,(100,100,0),(490,0,500,500))
    pygame.draw.rect(screen,(100,100,0),(0,0,10,500))
    pygame.display.flip()

pygame.quit()
sock.close()
t.join()