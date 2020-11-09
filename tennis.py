import pygame
import socket
import json
import threading
import queue
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "192.168.0.101"
PORT = 12345
pygame.init()

def sock_recv(cl,q):
    while True:
        try:
            R_data = cl.recv(10)
            R_data = R_data.decode("utf-8")
            R_data = json.loads(R_data)
            q.put(R_data)
        except:
            continue

q=queue.Queue()

# drawing window
screen = pygame.display.set_mode([500, 500])

# socket server, connect your game with 1 friend(client)
sock.bind((HOST, PORT))
sock.listen(1)
client, addr = sock.accept()

#parallely run listening to connected client

t=threading.Thread(target = sock_recv, args = (client, q))
t.start()

# original center
center = (250, 250)
center2 = (100, 100)
# Run until change in True condition
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # moving the circle with left clicks

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                center = pygame.mouse.get_pos()
        # dragging the circle with left click pushed

        if event.type==pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed() == (1,0,0):
                center = pygame.mouse.get_pos()
                S_data = json.dumps(center)
                client.send(bytes(S_data, encoding = "utf-8"))


    # background : white
    screen.fill((255, 255, 255))

    # colored circle the center
    if not q.empty():
        center2 = q.get()
        # print(center2.type())
    pygame.draw.circle(screen, (255, 0, 0), center, 10)
    pygame.draw.circle(screen, (255, 255, 0), center2, 10)

    # boundary
    pygame.draw.rect(screen,(255, 255, 0), (0, 490, 500, 500))
    pygame.draw.rect(screen, (255, 255, 0), (0, 0, 500, 10))
    pygame.draw.rect(screen, (255, 255, 0), (0, 0, 10, 500))
    pygame.draw.rect(screen, (255, 255, 0), (490, 0, 500, 500))

    # display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
t.join()
sock.close()