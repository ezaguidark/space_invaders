import pygame.font
import json
from pygame.sprite import Group

from ship_icon import Ship_2

class Scoreboard:
	""" muestra el score """

	def __init__(self, ai_game):
		"""inicia scorekeeping attributes"""
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats
		

		#font settings
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)


		#prepara la imagen inicial de score
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		""" Convierte el score en imagen renderizable"""
		rounded_score = round(self.stats.score, -1)
		score_str = f'{rounded_score:,}'
		self.score_image = self.font.render(score_str, True
				,self.text_color, self.settings.bg_color)

		# Display the score at the top right screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		""" Convierte el score en imagen renderizable"""
		high_score = round(self.stats.high_score, -1)
		high_score_str = f'{high_score:,}'
		self.high_score_image = self.font.render(f'High Score: {high_score_str}', True
				,self.text_color, self.settings.bg_color)

		# Display the score at the top right screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""Comprueba si el score es mas alto que el Highscore"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			with open('high_score.json', 'w') as file:
				json.dump(self.stats.high_score, file)
			self.prep_high_score()

	def show_score(self):
		"""Dibuja en pantalla"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def prep_level(self):
		"""Muestra el nivel actual"""
		level_str = str(self.stats.level)
		self.level_image = self.font.render(f'W: {level_str}', True,
			self.text_color, self.settings.bg_color)

		#posicion del texto
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_ships(self):
		""" Show how many ships are left"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship_2(self.ai_game)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)