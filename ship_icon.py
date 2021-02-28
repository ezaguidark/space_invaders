import pygame
from pygame.sprite import Sprite

class Ship_2(Sprite):
    """ clase inicia para la nave """

    def __init__(self, ai_game):        # ia_game al parecer es una variable que hace referencia
        """ iniciar la posicion inicial de la nave """  # a la clase principal del juego. puede tener cualquier nombre XD
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Cargar la imagen
        self.image = pygame.transform.scale(pygame.image.load('images/ship.png'), (40,40))
        self.rect = self.image.get_rect()

        