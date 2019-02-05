import pygame


pygame.init()
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
        print(event)
pygame.quit()
quit()