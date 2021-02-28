import pygame

class Sounds:
	def __init__(self):
		""" Cargar todos los sonidos"""
		self.shot = pygame.mixer.Sound('sounds/shot.wav')
		self.alien_hit = pygame.mixer.Sound('sounds/alien_hit.wav')
		self.bip = pygame.mixer.Sound('sounds/bip.ogg')
		self.bop = pygame.mixer.Sound('sounds/bop.ogg')
		self.play = pygame.mixer.Sound('sounds/play.mp3')
		self.loss = pygame.mixer.Sound('sounds/loss.wav')
		self.levelup = pygame.mixer.Sound('sounds/levelup.wav')
		self.gameover = pygame.mixer.Sound('sounds/gameover.wav')