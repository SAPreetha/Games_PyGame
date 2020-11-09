import pygame
pygame.init()
# drawing window
screen = pygame.display.set_mode([500, 500])

# original center
center = (250,250)
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
            if pygame.mouse.get_pressed()==(1,0,0):
                center = pygame.mouse.get_pos()


    # background : white
    screen.fill((255, 255, 255))

    # colored circle the center
    pygame.draw.circle(screen, (255, 0, 0), center, 75)

    # display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()