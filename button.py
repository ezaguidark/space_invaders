import pygame.font

class Button:
	def __init__(self, ai_game, msg):
		"""Atributos boton"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		# dimensiones button
		self.width, self.height = 400, 150
		self.button_color = (82, 98, 129)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Crear el rectangulo del boton
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# the button msg
		self._prep_msg(msg)


	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button."""
		self.msg_image = self.font.render(msg, True, self.text_color,
				self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Draw blank button and then draw message.
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)