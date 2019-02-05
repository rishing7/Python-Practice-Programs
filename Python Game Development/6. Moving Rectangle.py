import pygame


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

""" Needed canvas where we gonna draw our object so that we can play out there. """
gameDisplay = pygame.display.set_mode((800, 600))
""" Title of the game display basically name of the game. """
pygame.display.set_caption('Slither')
""" Flip/Update is done on every display. pygame.display.flip() can be used in place of pygame.display.update"""
pygame.display.update()
gameExit = False
lead_x = 300
lead_y = 300
while not gameExit:
    """ event is generated because of the display. """
    for event in pygame.event.get():
        # print(event)
        if event.type is pygame.QUIT:
            gameExit = True
        if event.type is pygame.KEYDOWN:
            if event.key is pygame.K_LEFT:
                lead_x -= 10
            if event.key is pygame.K_RIGHT:
                lead_x += 10

        gameDisplay.fill(white) # Color of the canvas
        pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, 10, 10])
        pygame.display.update()

pygame.quit()
quit()