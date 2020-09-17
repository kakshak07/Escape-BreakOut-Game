# Ben-Ryder 2019

import os
import pygame

import constants
import paths
import exceptions

import project.menus as menus
import project.game.controller as game
import project.editor.controller as editor


class ApplicationController:
    """ runs the whole application, changing section running based on states """
    def __init__(self):
        pygame.init()

        # Icon Setup
        icon = pygame.image.load(paths.imagePath + "icon.png")
        icon.set_colorkey((0, 0, 0))
        pygame.display.set_icon(icon)  # before set_mode as suggested in pygame docs

        # Display Setup
        self.display = pygame.display.set_mode(constants.DISPLAY_SIZE)  # only in menu. changes in game and editor
        pygame.display.set_caption(constants.DISPLAY_NAME)

        # General Setup
        self.state = "menu"
        self.game_reference = None

    def run(self):
        while self.state != "quit":
            if self.state == "menu":
                self.run_menu()

            elif self.state == "load_game":
                self.run_loadgame()

            elif self.state == "editor":
                self.run_editor()

            elif self.state == "game":
                self.run_game()

            else:
                raise exceptions.StateError("Invalid Game State: %s" % self.state)

        self.quit()

    def run_menu(self):
        menu = menus.Menu(self.display)  # takes control while section running, control returns here after.
        self.state = menu.get_state()

    def run_loadgame(self):
        load_game = menus.LoadGame(self.display)
        self.state = load_game.get_state()
        self.game_reference = load_game.get_game()

    def run_editor(self):
        running_editor = editor.Application()  # redefined to resize pygame.display
        self.state = running_editor.get_state()

        # resetting display, changed due to game resolution
        self.display = pygame.display.set_mode(constants.DISPLAY_SIZE)
        pygame.display.set_caption(constants.DISPLAY_NAME)

    def run_game(self):
        if self.game_reference is None:
            raise Exception("No Game Selected")

        # Checks for custom before loading built-in. This means if the same name is in custom and built-in, the program
        # will favour the custom one
        if os.path.isfile(paths.customGamePath + self.game_reference):
            running_game = game.Controller(paths.customGamePath + self.game_reference)
        else:
            running_game = game.Controller(paths.gamePath + self.game_reference)

        self.state = running_game.play()  # takes control, returns when game is complete.
        self.game_reference = None

        # resetting display, changed due to game resolution
        self.display = pygame.display.set_mode(constants.DISPLAY_SIZE)
        pygame.display.set_caption(constants.DISPLAY_NAME)

    def quit(self):
        pygame.quit()
        quit()






















