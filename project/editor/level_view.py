

import constants
import paths

import pygame
import pygame_gui

import project.game.search as search


class LevelView:
    def __init__(self, level):
        self.level = level

        self.image = {
            "path": pygame.image.load(paths.tilePath + "path.png"),
            "wall": pygame.image.load(paths.tilePath + "wall.png"),
            "spawn": pygame.image.load(paths.tilePath + "spawn-point.png"),
            "safe-point": pygame.image.load(paths.tilePath + "safe-point.png"),
            "exit-top": pygame.image.load(paths.tilePath + "exit-closed-top.png"),
            "exit-bottom": pygame.image.load(paths.tilePath + "exit-closed-bottom.png"),
            "exit-left": pygame.image.load(paths.tilePath + "exit-closed-left.png"),
            "exit-right": pygame.image.load(paths.tilePath + "exit-closed-right.png"),
            "key": pygame.image.load(paths.tilePath + "key.png"),

            "enemy-patrol": pygame.image.load(paths.tilePath + "enemy-patrol.png"),
            "enemy-random": pygame.image.load(paths.tilePath + "enemy-random.png"),
            "enemy-seeker": pygame.image.load(paths.tilePath + "enemy-seeker.png"),
        }

    def check_clicked(self, position):
        try:
            index_x = int(position[0]/self.level.TILE_SIZE)
            index_y = int(position[1]/self.level.TILE_SIZE)
            tile = self.level.format[index_x][index_y]  # getting value to beck on map
            return [index_x, index_y]
        except IndexError:
            return None

    def draw(self, display):
        self.draw_map(display)
        self.draw_keys(display)
        self.draw_enemies(display)
        self.draw_grid(display)  # not like game where draws below walls, should be above all.

    def draw_map(self, display):
        x = 0
        y = 0
        for row in self.level.format:
            for col in row:
                if col == "0":
                    display.blit(pygame.transform.scale(self.image["path"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "1":
                    display.blit(pygame.transform.scale(self.image["wall"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "p":
                    display.blit(pygame.transform.scale(self.image["spawn"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "s":
                    display.blit(pygame.transform.scale(self.image["safe-point"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "t":
                    display.blit(pygame.transform.scale(self.image["exit-top"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "b":
                    display.blit(pygame.transform.scale(self.image["exit-bottom"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "l":
                    display.blit(pygame.transform.scale(self.image["exit-left"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])
                elif col == "r":
                    display.blit(pygame.transform.scale(self.image["exit-right"],
                                                        [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])

                y += self.level.TILE_SIZE
            x += self.level.TILE_SIZE
            y = 0

    def draw_grid(self, display):
        for row in range(len(self.level.format) + 1):
            for col in range(len(self.level.format[1])):
                pygame.draw.line(display, constants.COLOURS["dark-gray"],
                                 [0, col * self.level.TILE_SIZE],
                                 [row * self.level.TILE_SIZE, col * self.level.TILE_SIZE], 1)

                pygame.draw.line(display, constants.COLOURS["dark-gray"],
                                 [row*self.level.TILE_SIZE, 0],
                                 [row*self.level.TILE_SIZE, self.level.DISPLAY_SIZE[1]], 1)

    def draw_keys(self, display):
        for key in self.level.keys:
            x = key[0] * self.level.TILE_SIZE
            y = key[1] * self.level.TILE_SIZE
            display.blit(pygame.transform.scale(self.image["key"],
                                                [self.level.TILE_SIZE, self.level.TILE_SIZE]), [x, y])

    def draw_enemies(self, display):
        for enemy in self.level.enemies:
            if enemy["type"] == "ep":
                x = enemy["patrol"][0][0] * self.level.TILE_SIZE + self.level.ENEMY_PADDING/2
                y = enemy["patrol"][0][1] * self.level.TILE_SIZE + self.level.ENEMY_PADDING/2
            else:
                x = enemy["spawn"][0] * self.level.TILE_SIZE + self.level.ENEMY_PADDING/2
                y = enemy["spawn"][1] * self.level.TILE_SIZE + self.level.ENEMY_PADDING/2

            if enemy["type"] == "ep":
                display.blit(pygame.transform.scale(self.image["enemy-patrol"],
                                                    [self.level.ENEMY_SIZE, self.level.ENEMY_SIZE]), [x, y])
            elif enemy["type"] == "er":
                display.blit(pygame.transform.scale(self.image["enemy-random"],
                                                    [self.level.ENEMY_SIZE, self.level.ENEMY_SIZE]), [x, y])
            elif enemy["type"] == "es":
                display.blit(pygame.transform.scale(self.image["enemy-seeker"],
                                                    [self.level.ENEMY_SIZE, self.level.ENEMY_SIZE]), [x, y])

    def draw_enemy_patrols(self, display):
        for enemy in [e for e in self.level.enemies if e["type"] == "ep"]:
            self.draw_patrol(display, enemy)

    def draw_patrol(self, display, enemy):
        patrol = enemy["patrol"]
        pause_text = pygame_gui.Text("", constants.FONTS["sizes"]["medium"], constants.FONTS["colour"],
                                     constants.FONTS["main"], 0, 0)

        previous_position = patrol[0]  # set to spawn
        for step in patrol[1:] + [patrol[0]]:  # spawn moved to end (as draw path from current to last position)
            if type(step) not in [int, float]:

                # Draw point on patrol position (of previous_position)
                pos = [round(previous_position[0] * self.level.TILE_SIZE + self.level.TILE_SIZE/2),
                        round(previous_position[1]*self.level.TILE_SIZE + self.level.TILE_SIZE/2)]
                pygame.draw.circle(display, (255, 255, 255), pos, round(self.level.TILE_SIZE/6))

                # Draw path from current to previous
                path = search.GridPath(self.level.format, step, previous_position, constants.WALL_FORMATS).get_path()
                if path is not None:  # as could be blocked if user adds a wall
                    self.draw_path(display, [step] + path)  # adding step to front so draws from previous_position

                previous_position = step.copy()  # otherwise will change to match step (mutable)

            else:
                pause_text.change_text(str(step))
                x = previous_position[0] * self.level.TILE_SIZE + 5
                y = previous_position[1] * self.level.TILE_SIZE
                pause_text.change_position(x, y)
                pause_text.draw(display)

    def draw_path(self, display, path):
        for step_index in range(len(path)-1):  # -1 as stopping at second to last, last is the final target.
            start = path[step_index]
            target = path[step_index + 1]

            start_point = [start[0] * self.level.TILE_SIZE + self.level.TILE_SIZE/2,
                           start[1] * self.level.TILE_SIZE + self.level.TILE_SIZE/2]

            target_point = [target[0] * self.level.TILE_SIZE + self.level.TILE_SIZE/2,
                           target[1] * self.level.TILE_SIZE + self.level.TILE_SIZE/2]

            pygame.draw.line(display, (255, 255, 255), start_point, target_point, 2)

