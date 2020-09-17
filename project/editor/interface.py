# Ben-Ryder 2019

import paths
import constants

import pygame
import pygame_gui


class SelectorButton(pygame_gui.Button):
    def draw(self, display):
        if self.mouse_over():
            self.hover_image.draw(display)
            pygame.draw.rect(display, (200, 200, 200), self.hover_image.rect, 1)
        else:
            self.rest_image.draw(display)


class Interface:
    def __init__(self, level, display):
        self.level = level
        self.left_option = None
        self.right_option = None
        self.patrol_focus = None

        # GUI Setup
        # Settings Buttons
        self.menu_button = pygame_gui.TextButton(
            [display.get_width() - self.level.EDITOR_SIZE, 0, self.level.EDITOR_SIZE, self.level.TILE_SIZE],
            (20, 20, 20), (40, 40, 40),
            "back to menu", 20, (200, 200, 200), constants.FONTS["main"])

        self.level_name = pygame_gui.RectEntry(
            [display.get_width() - self.level.EDITOR_SIZE,
             self.level.TILE_SIZE, self.level.EDITOR_SIZE, self.level.TILE_SIZE], 2,
            (255, 255, 255), (255, 255, 255),
            (160, 160, 160), (160, 160, 160),
            (255, 255, 255), (30, 100, 30),
            (160, 160, 160),  (30, 100, 30),
            "enter level name", 25, (0, 0, 0), constants.FONTS["main"],
            10, 5,
            False)

        self.save_button = pygame_gui.TextButton(
            [display.get_width() - self.level.EDITOR_SIZE/2, self.level.TILE_SIZE*2,
             self.level.EDITOR_SIZE/2, self.level.TILE_SIZE],
            (10, 40, 10), (20, 100, 20),
            "save", 20, (200, 200, 200), constants.FONTS["main"])

        self.load_button = pygame_gui.TextButton(
            [display.get_width() - self.level.EDITOR_SIZE, self.level.TILE_SIZE*2,
             self.level.EDITOR_SIZE/2, self.level.TILE_SIZE],
            (40, 40, 40), (60, 60, 60),
            "load", 20, (200, 200, 200), constants.FONTS["main"])

        self.tile_size = pygame_gui.RectEntry(
            [display.get_width() - self.level.EDITOR_SIZE,
             self.level.TILE_SIZE*3, self.level.TILE_SIZE, self.level.TILE_SIZE], 2,
            (255, 255, 255), (220, 220, 220),
            (160, 160, 160), (140, 140, 140),
            (255, 255, 255), (30, 100, 30),
            (160, 160, 160),  (30, 100, 30),
            str(self.level.TILE_SIZE), 25, (0, 0, 0), constants.FONTS["main"],
            8, 4,
            False)

        self.map_rows = pygame_gui.RectEntry(
            [display.get_width() - self.level.EDITOR_SIZE + self.level.TILE_SIZE,
             self.level.TILE_SIZE*3, self.level.TILE_SIZE, self.level.TILE_SIZE], 2,
            (255, 255, 255), (220, 220, 220),
            (160, 160, 160), (140, 140, 140),
            (255, 255, 255), (30, 100, 30),
            (160, 160, 160),  (30, 100, 30),
            str(self.level.MAP_SIZE[0]), 25, (0, 0, 0), constants.FONTS["main"],
            8, 4,
            False)

        self.map_columns = pygame_gui.RectEntry(
            [display.get_width() - self.level.EDITOR_SIZE + self.level.TILE_SIZE*2,
             self.level.TILE_SIZE*3, self.level.TILE_SIZE, self.level.TILE_SIZE], 2,
            (255, 255, 255), (220, 220, 220),
            (160, 160, 160), (140, 140, 140),
            (255, 255, 255), (30, 100, 30),
            (160, 160, 160),  (30, 100, 30),
            str(self.level.MAP_SIZE[1]), 25, (0, 0, 0), constants.FONTS["main"],
            8, 4,
            False)

        self.new = pygame_gui.TextButton(
            [display.get_width() - self.level.TILE_SIZE*3,
             self.level.TILE_SIZE*3, self.level.TILE_SIZE*3, self.level.TILE_SIZE],
            (100, 20, 20), (130, 30, 30),
            "new", 20, (200, 200, 200), constants.FONTS["main"])

        # Selector
        origin = [self.level.DISPLAY_SIZE[0], self.level.TILE_SIZE*5]
        padding = self.level.TILE_SIZE / 3

        self.path_button = SelectorButton(paths.tilePath + "path.png", paths.tilePath + "path.png",
                                             origin[0] + padding, origin[1])
        self.path_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.wall_button = SelectorButton(paths.tilePath + "wall.png", paths.tilePath + "wall.png",
                                             origin[0] + padding*5, origin[1])
        self.wall_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.spawn_button = SelectorButton(paths.tilePath + "spawn-point.png",
                                         paths.tilePath + "spawn-point.png",
                                         origin[0] + padding*10, origin[1])
        self.spawn_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.safe_button = SelectorButton(paths.tilePath + "safe-point.png",
                                        paths.tilePath + "safe-point.png",
                                        origin[0] + padding*14, origin[1])
        self.safe_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.exit_t_button = SelectorButton(paths.tilePath + "exit-closed-top.png",
                                        paths.tilePath + "exit-closed-top.png",
                                        origin[0] + padding, origin[1] + padding*4)
        self.exit_t_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.exit_b_button = SelectorButton(paths.tilePath + "exit-closed-bottom.png",
                                        paths.tilePath + "exit-closed-bottom.png",
                                        origin[0] + padding*5, origin[1] + padding*4)
        self.exit_b_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.exit_l_button = SelectorButton(paths.tilePath + "exit-closed-left.png",
                                        paths.tilePath + "exit-closed-left.png",
                                        origin[0] + padding*10, origin[1] + padding*4)
        self.exit_l_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.exit_r_button = SelectorButton(paths.tilePath + "exit-closed-right.png",
                                        paths.tilePath + "exit-closed-right.png",
                                        origin[0] + padding*14, origin[1] + padding*4)
        self.exit_r_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        self.key_button = SelectorButton(paths.tilePath + "key.png",
                                        paths.tilePath + "key.png",
                                        origin[0] + padding, origin[1] + padding*8)
        self.key_button.resize(self.level.TILE_SIZE, self.level.TILE_SIZE)

        # Enemy Selectors
        self.patrol_enemy_button = SelectorButton(paths.tilePath + "enemy-patrol.png",
                                        paths.tilePath + "enemy-patrol.png",
                                        origin[0] + padding, origin[1] + padding*13)

        self.random_enemy_button = SelectorButton(paths.tilePath + "enemy-random.png",
                                        paths.tilePath + "enemy-random.png",
                                        origin[0] + padding*5, origin[1] + padding*13)

        self.seeker_enemy_button = SelectorButton(paths.tilePath + "enemy-seeker.png",
                                        paths.tilePath + "enemy-seeker.png",
                                        origin[0] + padding*9, origin[1] + padding*13)

        # Patrol Entry Options (only active if self.patrol_focus is not None)
        self.patrol_focus_indicator = pygame_gui.Label([display.get_width() - self.level.EDITOR_SIZE,
                                                        origin[1] + padding*16,
                                                        self.level.EDITOR_SIZE, self.level.TILE_SIZE],
                                                       (60, 60, 60), (60, 60, 60),
                                                       "Inputting Patrol",
                                                       constants.FONTS["sizes"]["large"],
                                                       constants.FONTS["colour"],
                                                       constants.FONTS["main"])

        self.patrol_reset_button = pygame_gui.TextButton(
            [display.get_width() - self.level.EDITOR_SIZE, origin[1] + padding*19,
             self.level.EDITOR_SIZE/2, self.level.TILE_SIZE],
            (100, 20, 20), (130, 30, 30),
            "reset", 20, (200, 200, 200), constants.FONTS["main"])

        self.patrol_confirm_button = pygame_gui.TextButton(
            [display.get_width() - self.level.EDITOR_SIZE/2, origin[1] + padding*19,
             self.level.EDITOR_SIZE/2, self.level.TILE_SIZE],
            (10, 40, 10), (20, 100, 20),
            "confirm", 20, (200, 200, 200), constants.FONTS["main"])

        # Toggle Buttons
        self.show_keys = True
        self.show_key_button = pygame_gui.TextButton(
            [self.level.DISPLAY_SIZE[0], self.level.DISPLAY_SIZE[1] - self.level.TILE_SIZE,
             self.level.EDITOR_SIZE/2, self.level.TILE_SIZE],
            (40, 40, 40), (60, 60, 60),
            "toggle keys", 17, (200, 200, 200), constants.FONTS["main"])

        self.show_patrols = True
        self.show_patrols_button = pygame_gui.TextButton(
            [self.level.DISPLAY_SIZE[0] + self.level.EDITOR_SIZE/2, self.level.DISPLAY_SIZE[1] - self.level.TILE_SIZE,
             self.level.EDITOR_SIZE/2, self.level.TILE_SIZE],
            (40, 40, 40), (60, 60, 60),
            "toggle patrols", 17, (200, 200, 200), constants.FONTS["main"])

    def display_keys(self):
        return self.show_keys

    def display_patrols(self):
        return self.show_patrols

    def get_option(self, mouse_button):
        if mouse_button == "left":
            return self.left_option
        elif mouse_button == "right":
            return self.right_option
        else:
            raise Exception("invalid mouse_button given")

    def get_patrol_focus(self):
        return self.patrol_focus

    def set_patrol_focus(self, focus):
        self.patrol_focus = focus

    def refresh(self, level, display):
        filename = self.level_name.text.text
        self.__init__(level, display)
        self.level_name.text.change_text(filename)
        self.level_name.center_text()  # wont be auto-done when manually changing text

    def check_clicked(self, position, mouse_button):
        result = None
        new_option = None

        # Settings
        if self.menu_button.check_clicked():
            result = "menu"
        elif self.save_button.check_clicked():
            result = "save"
        elif self.load_button.check_clicked():
            result = "load"
        elif self.new.check_clicked():
            result = "new"

        # Brush Options
        elif self.path_button.check_clicked():
            new_option = "0"
        elif self.wall_button.check_clicked():
            new_option = "1"
        elif self.spawn_button.check_clicked():
            new_option = "p"
        elif self.safe_button.check_clicked():
            new_option = "s"
        elif self.exit_t_button.check_clicked():
            new_option = "t"
        elif self.exit_b_button.check_clicked():
            new_option = "b"
        elif self.exit_l_button.check_clicked():
            new_option = "l"
        elif self.exit_r_button.check_clicked():
            new_option = "r"
        elif self.key_button.check_clicked():
            new_option = "k"

        elif self.patrol_enemy_button.check_clicked():
            new_option = "ep"  # patrol_focus set by controller if it adds a patrol
        elif self.random_enemy_button.check_clicked():
            new_option = "er"
        elif self.seeker_enemy_button.check_clicked():
            new_option = "es"

        elif self.show_key_button.check_clicked():
            self.show_keys = not self.show_keys
        elif self.show_patrols_button.check_clicked():
            self.show_patrols = not self.show_patrols

        if new_option is not None:
            if mouse_button == "left":
                self.left_option = new_option
            elif mouse_button == "right":
                self.right_option = new_option

        if self.patrol_focus is not None:
            if self.patrol_reset_button.check_clicked():
                result = "patrol-reset"
            elif self.patrol_confirm_button.check_clicked():
                self.patrol_focus = None

        self.level_name.check_clicked()
        self.tile_size.check_clicked()
        self.map_rows.check_clicked()
        self.map_columns.check_clicked()

        return result  # result (quit, menu etc)
        # also update option if selector clicked

    def handle_keydown(self, event):
        self.level_name.handle_event(event)
        self.tile_size.handle_event(event)
        self.map_rows.handle_event(event)
        self.map_columns.handle_event(event)

    def handle_keyup(self, event):
        self.level_name.handle_event_up(event)
        self.tile_size.handle_event_up(event)
        self.map_rows.handle_event_up(event)
        self.map_columns.handle_event_up(event)

    def get_filename(self):
        return self.level_name.text.text

    def get_map_size(self):
        try:
            rows = int(self.map_rows.text.text)
            cols = int(self.map_columns.text.text)
            return [rows, cols]
        except ValueError:
            return None

    def get_tile_size(self):
        try:
            return int(self.tile_size.text.text)
        except ValueError:
            return None

    def draw(self, display):
        self.menu_button.draw(display)
        self.level_name.draw(display)
        self.save_button.draw(display)
        self.load_button.draw(display)
        self.tile_size.draw(display)
        self.map_rows.draw(display)
        self.map_columns.draw(display)
        self.new.draw(display)

        # Tile Option Selectors
        self.path_button.draw(display)
        self.wall_button.draw(display)
        self.spawn_button.draw(display)
        self.safe_button.draw(display)
        self.exit_t_button.draw(display)
        self.exit_b_button.draw(display)
        self.exit_l_button.draw(display)
        self.exit_r_button.draw(display)

        self.key_button.draw(display)
        self.patrol_enemy_button.draw(display)
        self.random_enemy_button.draw(display)
        self.seeker_enemy_button.draw(display)

        if self.patrol_focus is not None:
            self.patrol_focus_indicator.draw(display)
            self.patrol_reset_button.draw(display)
            self.patrol_confirm_button.draw(display)

        self.show_key_button.draw(display)
        self.show_patrols_button.draw(display)



#
#         # Patrol Inputting
#         self.allow_patrol_input = False
#         self.enemy_editing = None
#         self.patrol_input = pygame_gui.RectEntry(
#             [0, self.level.DISPLAY_SIZE[1] - self.level.TILE_SIZE,
#              self.level.DISPLAY_SIZE[0] - self.level.TILE_SIZE*2, self.level.TILE_SIZE], 2,
#             (255, 255, 255), (255, 255, 255),
#             (160, 160, 160), (160, 160, 160),
#             (255, 255, 255), (30, 100, 30),
#             (160, 160, 160),  (30, 100, 30),
#             "", 25, (0, 0, 0), constants.FONTS["main"],
#             10, 5,
#             True)
#         self.submit_patrol_button = pygame_gui.TextButton(
#             [self.level.DISPLAY_SIZE[0] - self.level.TILE_SIZE*2, self.level.DISPLAY_SIZE[1] - self.level.TILE_SIZE,
#              self.level.TILE_SIZE*2, self.level.TILE_SIZE],
#             (20, 20, 20), (40, 40, 40),
#             "submit", 20, (200, 200, 200), constants.FONTS["main"])
#