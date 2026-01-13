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
