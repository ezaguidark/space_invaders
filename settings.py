class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)
        self.bg_x_pos = 0
        

        # Ship settings
        self.ship_limit = 3  # Vidas restantes de la nave

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (109, 255, 149)
        self.bullets_allowed = 4

        # Alien settings
        self.fleet_drop_speed = 15
        

        # How quickly the game speeds up
        self.speedup_scale = 1.5
        self.initialize_dynamic_settings()

        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Scoring
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """settings que cambian a lo largo del juego"""
        self.ship_speed = 2.5
        self.bullet_speed = 5.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Incrementa la velocidad de las cosas"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        # tambien aumenta la puntuacion.
        self.alien_points = int(self.alien_points * self.score_scale)
