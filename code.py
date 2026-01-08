#!usr/bin/env python3
"""
Created by: Linh Huynh
Created on: Jan 2026
This is final project of TEJ4M course
Refactored to OOP for "Space Aliens" game
"""

import ugame
import stage
import time
import random
import supervisor

import constants


class SpaceAliensGame:
    def important_stuffs(self):
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

    def splash_scene(self):
        """this function shows the scene"""
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
        # Text that will appear on the screen
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
        self._update_score_text()

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
        self._spawn_alien()

        # Lasers
        self.lasers = [stage.Sprite(self.image_bank_sprites, 10,
                                    constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        for _ in range(constants.TOTAL_NUMBER_OF_LASERS)]

        # Add layers
        self.game.layers = [self.score_text] + self.lasers + [self.ship] + self.aliens + [background]
        self.game.render_block()

        # Main game loop
        while True:
            self._handle_input()
            self._update_lasers()
            self._update_aliens()
            self._check_collisions()
            self.game.render_sprites(self.lasers + [self.ship] + self.aliens)
            self.game.tick()
