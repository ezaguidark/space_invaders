import sys
from time import sleep

import pygame, json

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from sounds import Sounds


bg_space = pygame.transform.scale(pygame.image.load('images/space.jpg'), (1200,700))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


class AlienInvasion:
    """ La clase principal que representa al juego"""

    def __init__(self):
        """ iniciando el juego y recursos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion by David")

        self.bg_x = self.settings.bg_x_pos 

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.sounds = Sounds()

        self.alien = Alien(self)
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # crea el boton
        self.play_button = Button(self, 'Jugar')

        # crea una instancia de game stats
        self.stats = GameStats(self)
        # crea una insancia de Score
        self.sb = Scoreboard(self)



    def run_game(self):
        """ start the main loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self._move_bg()


            # Make the most recently drawn screen visible.
            pygame.display.flip()
            
    def _check_events(self):
        # ver eventos del teclado y mouse
            for event in pygame.event.get():  # Esto es algo asi como una lista de valores de eventos, la funcion .get() los recopila.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                


    def _check_keydown_events(self, event):
        """responde a keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """comienza el juego cuando el jugador clickea"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            # reset the game
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # tambien
            self.aliens.empty()
            self.bullets.empty()

            # crea nuevamente las naves
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
            self.sounds.play.play()

    def _fire_bullet(self):
        """ crea una bala y la agrega al grupo"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sounds.shot.play()
        
    def _update_bullets(self):
        """update la posicionde las balas y elimina las antiguas"""
        # Update position
        self.bullets.update()

        # Elimina las balas que salen del borde
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sounds.alien_hit.play()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #aumenta el numero del nivel
            self.sounds.levelup.play()
            sleep(2)
            self.stats.level += 1
            self.sb.prep_level()


    def _move_bg(self):
    	self.bg_x += 0.5
    	if self.bg_x == 1200:
    		self.bg_x = 0

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
        (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create full flet.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)	

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Chequea colisiones
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # verifica si tocna fondo 
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        if self.settings.fleet_direction == 1:
            self.sounds.bip.play()
        else:
            self.sounds.bop.play()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(bg_space, (self.bg_x , 0))
        self.screen.blit(bg_space, (self.bg_x - 1200, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Draw the score information
        self.sb.show_score()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _ship_hit(self):
        """responde a colision nave alien"""
        if self.stats.ships_left > 0:
            # Decrement Ship left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Elimina aliens restantes
            self.aliens.empty()
            self.bullets.empty()

            # crea de nuevo naves y aliens
            self._create_fleet()
            self.ship.center_ship()

            # pause
            self.sounds.loss.play()
            sleep(3) # esto es de time.sleep
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sounds.gameover.play()

    def _check_aliens_bottom(self):
        """Check si un alien llega al fondo"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game ?
    ai = AlienInvasion()
    ai.run_game()
