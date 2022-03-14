import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
color = 255
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if screen.get_width()/2 - 50 <= pos[0] and screen.get_width()/2 + 50 >= pos[0]:
                if color == 255:
                    color = 0
                else:
                    color = 255


    # Fill the background with white 
    screen.fill((255, 255, 254))

    # Draw a solid blue circle in the center test
    pygame.draw.rect(screen, (0,0,color), (200, 150, 100, 50))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
