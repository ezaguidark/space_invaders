import json

class GameStats:
	"""Track statistics for Alien Invasion."""
	def __init__(self, ai_game):
		"""Initialize statistics."""
		self.settings = ai_game.settings
		self.reset_stats()
		# Start Alien Invasion in an active state.
		self.game_active = False
		# High score
		try:
			with open('high_score.json') as file:
				self.high_score = json.load(file)
		except:
			self.high_score = 0

	def reset_stats(self):
		"""Initialize statistics that can change during the game."""
		# Vidas restantes de la nave
		#por algun motivo, el valor esta en settings pero se referencia aqui tambien.
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1