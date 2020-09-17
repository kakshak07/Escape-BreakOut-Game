# (not ready)

# This Editor is specific to my game Sense (see github.com/Ben-Ryder/Sense), although could be adapted and simplified
# to create a simple tiled based, with "walls and paths", ie 2 choices for the tile.
import os
import pygame

import constants
import paths

import project.editor.level as level
import project.editor.level_view as level_view
import project.editor.interface as interface


class Stopwatch:  # starts tracking from point of declaration.
    def __init__(self):
        self.start = pygame.time.get_ticks()

    def get_time(self):  # returned in seconds
        return (pygame.time.get_ticks() - self.start) / 1000

    def reset(self):
        self.start = pygame.time.get_ticks()


class Application:
    def __init__(self):
        self.state = "editor"

        pygame.display.set_caption(constants.DISPLAY_NAME + " - " + "Level Editor")

        # Level Setup
        self.level = level.LevelModel()
        self.level_view = level_view.LevelView(self.level)

        self.display = pygame.display.set_mode([self.level.DISPLAY_SIZE[0] + self.level.EDITOR_SIZE,
                                                self.level.DISPLAY_SIZE[1]])

        self.editor_interface = interface.Interface(self.level, self.display)  # needs display to size accordingly (no-link)
        # editor passed level for access to tile and map size. DOESNT EDIT THEM, THIS IS THOUGH CONTROLLER (no-link)

        self.left_brush = False  # whether or not to edit the map
        self.right_brush = False

        self.patrol_timer = Stopwatch()  # for timing duration of mouse down for adding pause to patrol

        self.run()

    def run(self):
        while self.state not in ["menu", "quit"]:  # could close application, or return to menu
            self.handle_events()
            self.draw()

    def get_state(self):
        return self.state

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"

            elif event.type == pygame.KEYDOWN:
                self.editor_interface.handle_keydown(event)

            elif event.type == pygame.KEYUP:
                self.editor_interface.handle_keyup(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.brushes_off()

                if event.button == 1:
                    self.left_brush_on()
                    mouse_button = "left"
                elif event.button == 3:
                    self.right_brush_on()
                    mouse_button = "right"
                else:
                    mouse_button = "middle"

                if mouse_button != "middle" and self.editor_interface.get_option(mouse_button) == "ep" and \
                        self.editor_interface.get_patrol_focus() is not None and \
                        self.level_view.check_clicked(pygame.mouse.get_pos()) is not None:  # ie, clicked in map area
                    time = self.patrol_timer.get_time() - 0.5
                    if time > 0:  # must hold down mouse for over a second to start timer
                        self.level.patrol_append(self.editor_interface.get_patrol_focus(), round(time, 1))
                        self.patrol_timer.reset()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if event.button == 1:
                    self.left_brush_on()
                    mouse_button = "left"
                elif event.button == 3:
                    self.right_brush_on()
                    mouse_button = "right"
                else:
                    mouse_button = "middle"

                # Checking for enemy and key inputting on map (don't want continuous inputs)
                tile_clicked = self.level_view.check_clicked(mouse)
                if tile_clicked is not None and mouse_button != "middle":
                    option = self.editor_interface.get_option(mouse_button)  # mouse_size is "left" or "right"

                    if option == "ep":  # type int means adding pause to current patrol
                        self.patrol_timer.reset()
                        if not self.level.is_wall(tile_clicked):
                            if self.editor_interface.get_patrol_focus() is None:
                                self.level.add_patrol_enemy(tile_clicked)
                                self.editor_interface.set_patrol_focus(tile_clicked)
                                # tile_clicked becomes key of enemy
                            else:
                                self.level.patrol_append(self.editor_interface.get_patrol_focus(), tile_clicked)
                                # wil run error check if it should actually add it in level

                    elif option == "es":
                        if not self.level.is_wall(tile_clicked):
                            self.level.add_seeker_enemy(tile_clicked)

                    elif option == "er":
                        if not self.level.is_wall(tile_clicked):
                            self.level.add_random_enemy(tile_clicked)

                    elif option == "k":  # adding a key
                        if not self.level.is_wall(tile_clicked):
                            self.level.add_key(tile_clicked)

                # Checking for settings changes (save, back, map name etc)
                result = self.editor_interface.check_clicked(mouse, mouse_button)  # will update option for map brushes
                if result == "menu":
                    self.state = "menu"

                elif result == "load":
                    filename = self.editor_interface.get_filename()
                    if self.editor_interface.get_filename() != "":
                        if os.path.isfile(paths.customGamePath + filename):
                            self.level.load(paths.customGamePath + filename)

                        elif os.path.isfile(paths.gamePath + filename):
                            self.level.load(paths.gamePath + filename)

                        self.refresh_view()

                elif result == "save":
                    filename = self.editor_interface.get_filename()
                    if filename != "" and filename[:6] != "Level " and \
                            self.editor_interface.get_filename() != "enter level name":
                        self.level.save(paths.customGamePath + self.editor_interface.get_filename())
                        self.state = "menu"

                elif result == "new":
                    new_tile_size = self.editor_interface.get_tile_size()
                    new_map_size = self.editor_interface.get_map_size()
                    if new_map_size is not None and new_tile_size is not None:  # if None error in converting to int
                        self.level.change_tile_size(new_tile_size)
                        self.level.change_map_size(new_map_size)

                        self.level.set_blank()
                        self.refresh_view()

                elif result == "patrol-reset":
                    # indicates re-setting a patrol enemies patrol (done once and not as a brush so here)
                    self.level.clear_patrol(self.editor_interface.get_patrol_focus())

                elif result is not None:
                    raise Exception("Invalid result for editor interface")

        # Checking for brush input of map tiles
        if self.left_brush or self.right_brush:
            # Checking for tile changes on map
            mouse = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()  # repeated in-case for loop doesnt run.
            if mouse_pressed[0]:
                mouse_button = "left"
            elif mouse_pressed[2]:
                mouse_button = "right"
            else:
                mouse_button = "middle"

            tile_clicked = self.level_view.check_clicked(mouse)
            if tile_clicked is not None and mouse_button != "middle" and self.editor_interface.get_patrol_focus() is None:
                option = self.editor_interface.get_option(mouse_button)  # mouse_size is "left" or "right"

                if option in constants.WALL_FORMATS + ["0"]:  # adding path, as still a tile.
                    self.level.clear_tile(tile_clicked)  # delete enemy or key if on tile
                    if self.level.allow_wall(tile_clicked):  # will not allow if a patrol point of enemy
                        self.level.change_tile(tile_clicked, option)

                elif option not in ["ep", "ep-", "er", "es", "k"] and option is not None:
                    raise Exception("Invalid option for map edit")

    def left_brush_on(self):
        self.left_brush = True
        self.right_brush = False

    def right_brush_on(self):
        self.right_brush = True
        self.left_brush = False

    def brushes_off(self):
        self.right_brush = False
        self.left_brush = False

    def refresh_view(self):
        self.display = pygame.display.set_mode([self.level.DISPLAY_SIZE[0] + self.level.EDITOR_SIZE,
                                                self.level.DISPLAY_SIZE[1]])
        self.editor_interface.refresh(self.level, self.display)
        # level view will auto adapt, but editor interface must refresh to change size accordingly.

    def draw(self):
        self.display.fill((20, 20, 20))

        # Drawing level (separate bits to isolate keys and enemies to allow for drawing choice)
        self.level_view.draw_map(self.display)
        self.level_view.draw_grid(self.display)  # not like game where draws below walls, should be above all.

        if self.editor_interface.display_patrols():
            self.level_view.draw_enemy_patrols(self.display)
        else:
            # draw only the specific enemy
            if self.editor_interface.get_patrol_focus() is not None:
                enemy = self.level.get_enemy(self.editor_interface.get_patrol_focus())
                self.level_view.draw_patrol(self.display, enemy)

        self.level_view.draw_enemies(self.display)

        if self.editor_interface.display_keys():
            self.level_view.draw_keys(self.display)

        self.editor_interface.draw(self.display)
        pygame.display.update()
