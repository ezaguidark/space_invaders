import pygame
from pygame.sprite import Sprite

pygame.init()

class Alien(Sprite):
	"""A class to represent a single alien in the fleet."""
	def __init__(self, ai_game):
		"""Initialize the alien and set its starting position."""
		super().__init__()
		self.screen = ai_game.screen
		# Load the alien image and set its rect attribute.
		self.index = 0
		self.counter = 0
		self.image1 = pygame.transform.scale(pygame.image.load('images/alien1.png'), (60, 60))
		self.image2 = pygame.transform.scale(pygame.image.load('images/alien2.png'), (60, 60))
		self.frames = [self.image1, self.image2]
		self.image = self.frames[self.index]
		self.rect = self.image.get_rect()
		self.settings = ai_game.settings
		# Start each new alien near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		# Store the alien's exact horizontal position.
		self.x = float(self.rect.x)

	def check_edges(self):
		"""Return True if alien is at edge of screen."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True


	def update(self):
		# intento de animar los aliens
		self.counter += 1
		if self.counter == 50:
			self.index += 1
			self.counter = 0
		if self.index >= len(self.frames):
			self.index = 0
		self.image = self.frames[self.index]
		"""Move the alien right or left."""
		self.x += (self.settings.alien_speed *self.settings.fleet_direction)
		self.rect.x = self.x

	
