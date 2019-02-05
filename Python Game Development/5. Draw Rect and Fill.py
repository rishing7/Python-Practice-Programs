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
while not gameExit:
    """ event is generated because of the display. """
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            gameExit = True

        gameDisplay.fill(white) # Color of the canvas
        pygame.draw.rect(gameDisplay, black, [400, 300, 10, 10])
        # pygame.draw.rect(gameDisplay, red, [400, 300, 10, 10])
        gameDisplay.fill(red, rect=[200, 200, 50, 50])
        pygame.display.update()

pygame.quit()
quit()