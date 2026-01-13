#!usr/bin/env python3
"""
Created by: Linh Huynh
Created on: Jan 2026
Refactored to OOP for "Space Aliens" game
"""

import ugame
import stage
import time
import random
import supervisor

import constants


class SpaceAliensGame:
    def important_stuff(self):
        # Game attributes
        self.score = 0
        self.ship = None
        self.aliens = []
        self.lasers = []
        self.a_button = constants.button_state["button_up"]
        self.b_button = constants.button_state["button_up"]
        self.start_button = constants.button_state["button_up"]
        self.select_button = constants.button_state["button_up"]

        # Sounds
        self.sound = ugame.audio
        self.pew_sound = open("pew.wav",'rb')
        self.boom_sound = open("boom.wav",'rb')
        self.crash_sound = open("crash.wav",'rb')
        self.coin_sound = open("coin.wav",'rb')

        # Image banks
        self.image_bank_bg = stage.Bank.from_bmp16("space_aliens_background.bmp")
        self.image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")
        self.image_bank_mt = stage.Bank.from_bmp16("mt_game_studio.bmp")

        # Stage
        self.game = stage.Stage(ugame.display, constants.FPS)
        self.game.layers = []

    def run(self):
        self.splash_scene()

    # ------------------ Scenes ------------------ #
    def splash_scene(self):
        background = stage.Grid(self.image_bank_mt, constants.SCREEN_X, constants.SCREEN_Y)
        self.game.layers = [background]
        self.game.render_block()
        time.sleep(2.0)
        self.menu_scene()

    def menu_scene(self):
        background = stage.Grid(self.image_bank_mt, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
        # set tiles
        for y in range(2, 6):
            for x, tile in enumerate([0, 1, 2, 3, 4, 0] if y==2 else
                                     [0, 5, 6, 7, 8, 0] if y==3 else
                                     [0, 9, 10, 11, 12, 0] if y==4 else
                                     [0, 0, 13, 14, 0, 0]):
                background.tile(x+2, y, tile)
        # Text
        text_layers = []
        title_text = stage.Text(width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer=None)
        title_text.move(20,10)
        title_text.text("Space Alien Game")
        text_layers.append(title_text)

        start_text = stage.Text(width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None)
        start_text.move(35,110)
        start_text.text("PRESS START")
        text_layers.append(start_text)

        # Play coin sound
        self.sound.stop()
        self.sound.mute(False)
        self.sound.play(self.coin_sound)

        self.game.layers = text_layers + [background]
        self.game.render_block()

        # Wait for START button
        while True:
            keys = ugame.buttons.get_pressed()
            if keys & ugame.K_START != 0:
                self.game_scene()

    def game_scene(self):
        self.score = 0
        # Score text
        self.score_text = stage.Text(width=29, height=14, font=None, palette=constants.RED_PALETTE, buffer=None)
        self.score_text()

        # Background
        background = stage.Grid(self.image_bank_bg, constants.SCREEN_X, constants.SCREEN_Y)
        for x in range(constants.SCREEN_GRID_X):
            for y in range(constants.SCREEN_GRID_Y):
                background.tile(x, y, random.randint(1,3))

        # Ship
        self.ship = stage.Sprite(self.image_bank_sprites, 5,
                                 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

        # Aliens
        self.aliens = [stage.Sprite(self.image_bank_sprites, 9,
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                       for _ in range(constants.TOTAL_NUMBER_OF_ALIENS)]
        self.spawn_alien()

        # Lasers
        self.lasers = [stage.Sprite(self.image_bank_sprites, 10,
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                       for _ in range(constants.TOTAL_NUMBER_OF_LASERS)]

        # Add layers
        self.game.layers = [self.score_text] + self.lasers + [self.ship] + self.aliens + [background]
        self.game.render_block()

        # Main game loop
        while True:
            self.handle_input()
            self.show_lasers()
            self.show_aliens()
            self.check_collisions()
            self.game.render_sprites(self.lasers + [self.ship] + self.aliens)
            self.game.tick()

    def game_over_scene(self):
        self.sound.stop()
        background = stage.Grid(self.image_bank_mt, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
        text_layers = []

        score_text = stage.Text(width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None)
        score_text.move(22,20)
        score_text.text("Final Score: {:0>2d}".format(self.score))
        text_layers.append(score_text)

        over_text = stage.Text(width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None)
        over_text.move(43,60)
        over_text.text("GAME OVER")
        text_layers.append(over_text)

        select_text = stage.Text(width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None)
        select_text.move(32,110)
        select_text.text("PRESS SELECT")
        text_layers.append(select_text)

        self.game.layers = text_layers + [background]
        self.game.render_block()

        while True:
            keys = ugame.buttons.get_pressed()
            if keys & ugame.K_SELECT != 0:
                supervisor.reload()
            self.game.tick()

    # ------------------ Private Methods ------------------ #
    def score_text(self):
        self.score_text.clear()
        self.score_text.cursor(0,0)
        self.score_text.move(1,1)
        self.score_text.text("Score:{0}".format(self.score))

    def spawn_alien(self):
        for alien in self.aliens:
            if alien.x < 0:
                alien.move(random.randint(constants.SPRITE_SIZE, constants.SCREEN_X - constants.SPRITE_SIZE),
                           constants.OFF_TOP_SCREEN)
                break

    def handle_input(self):
        keys = ugame.buttons.get_pressed()

        # Button A
        if keys & ugame.K_O != 0:
            if self.a_button == constants.button_state["button_up"]:
                self.a_button = constants.button_state["button_just_pressed"]
            elif self.a_button == constants.button_state["button_just_pressed"]:
                self.a_button = constants.button_state["button_still_pressed"]
        else:
            if self.a_button == constants.button_state["button_still_pressed"]:
                self.a_button = constants.button_state["button_released"]
            else:
                self.a_button = constants.button_state["button_up"]

        # Movement
        if keys & ugame.K_RIGHT != 0:
            self.ship.move(min(self.ship.x + constants.SPRITE_MOVEMENT_SPEED, constants.SCREEN_X - constants.SPRITE_SIZE),
                           self.ship.y)
        if keys & ugame.K_LEFT != 0:
            self.ship.move(max(self.ship.x - constants.SPRITE_MOVEMENT_SPEED, 0),
                           self.ship.y)

        # Fire laser
        if self.a_button == constants.button_state["button_just_pressed"]:
            for laser in self.lasers:
                if laser.x < 0:
                    laser.move(self.ship.x, self.ship.y)
                    self.sound.play(self.pew_sound)
                    break

    def show_lasers(self):
        for laser in self.lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

    def show_aliens(self):
        for alien in self.aliens:
            if alien.x > 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    self.spawn_alien()
                    self.score = max(0, self.score - 1)
                    self.score_text()

    def check_collisions(self):
        # Laser hits alien
        for laser in self.lasers:
            if laser.x > 0:
                for alien in self.aliens:
                    if alien.x > 0 and stage.collide(laser.x + 6, laser.y + 2,
                                                    laser.x + 11, laser.y + 12,
                                                    alien.x + 1, alien.y,
                                                    alien.x + 15, alien.y + 15):
                        alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        self.sound.stop()
                        self.sound.play(self.boom_sound)
                        self.spawn_alien()
                        self.spawn_alien()
                        self.score += 1
                        self.score_text()
        # Alien hits ship
        for alien in self.aliens:
            if alien.x > 0 and stage.collide(alien.x + 1, alien.y,
                                            alien.x + 15, alien.y + 15,
                                            self.ship.x, self.ship.y,
                                            self.ship.x + 15, self.ship.y + 15):
                self.sound.stop()
                self.sound.play(self.crash_sound)
                time.sleep(3.0)
                self.game_over_scene()


if __name__ == "__main__":
    game = SpaceAliensGame()
    game.run()
