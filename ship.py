import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """ clase inicia para la nave """

    def __init__(self, ai_game):        # ia_game al parecer es una variable que hace referencia
        """ iniciar la posicion inicial de la nave """  # a la clase principal del juego. puede tener cualquier nombre XD
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Cargar la imagen
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Flag Movimiento
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """al parecer actualiza la posicion de movimiento si es True"""
        # ahora actualiza el valir de x en ship
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  # la velocidad fijada en settings de 1.5
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # entonces rect object se actualiza desde self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center ship n the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
