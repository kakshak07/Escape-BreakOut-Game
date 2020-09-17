
import os

import paths

import project.data as data


class LevelModel:
    def __init__(self, filename=None):
        if filename is not None and os.path.isfile(paths.dataPath + filename):
            self.load(filename)
        else:
            # Default values if not loading file
            self.TILE_SIZE = 50
            self.MAP_SIZE = [20, 14]

            self.format = None
            self.set_blank()

            # Keys Setup
            self.keys = []

            # Enemies Setup
            self.enemies = []

        # Sizing Setup (All based of map and tile size, so same if default or loaded)
        self.DISPLAY_SIZE = None
        self.EDITOR_SIZE = None

        self.PLAYER_SIZE = None
        self.PLAYER_PADDING = None

        self.ENEMY_SIZE = None
        self.ENEMY_PADDING = None
        self.set_sizes()  # all set in this function, but set to None so defined in __init__ method

    def load(self, filename):
        levelData = data.load(filename)

        # Setting Display and General Sizes based of Tile Resolution
        self.TILE_SIZE = levelData["tile-size"]
        self.MAP_SIZE = levelData["map-size"]

        self.set_sizes()

        self.format = levelData["map-format"]
        self.keys = levelData["keys"]
        self.enemies = levelData["enemies"]

    def set_sizes(self):
        self.DISPLAY_SIZE = [self.TILE_SIZE * self.MAP_SIZE[0], self.TILE_SIZE * self.MAP_SIZE[1]]
        self.EDITOR_SIZE = self.TILE_SIZE * 6

        self.PLAYER_SIZE = round(0.7 * self.TILE_SIZE)
        self.PLAYER_PADDING = self.TILE_SIZE - self.PLAYER_SIZE

        self.ENEMY_SIZE = round(0.5 * self.TILE_SIZE)
        self.ENEMY_PADDING = self.TILE_SIZE - self.ENEMY_SIZE

    def set_blank(self):
        # Format Setup (setting up blank 2d-array based on map size)
        self.format = [
            ["0" for row in range(self.MAP_SIZE[1])] for col in range(self.MAP_SIZE[0])
        ]

        # Applying wall around map outside
        # Top and Bottom Wall
        for row in self.format:
            row[0] = "1"
            row[len(row) - 1] = "1"

        # Left Wall
        index = 0
        for tile in self.format[0]:
            self.format[0][index] = "1"
            index += 1

        # Right Wall
        index = 0
        for tile in self.format[len(self.format) - 1]:
            self.format[len(self.format) - 1][index] = "1"
            index += 1

        self.enemies = []
        self.keys = []

    def save(self, filename):
        level = {
            "tile-size": self.TILE_SIZE,
            "map-size": self.MAP_SIZE,

            "map-format": self.format,
            "keys": self.keys,
            "enemies": self.enemies,
        }
        try:
            data.save(level, filename)
            return True
        except IsADirectoryError:
            return False

    def change_tile_size(self, new):
        self.TILE_SIZE = new
        self.set_sizes()

    def change_map_size(self, new):
        self.MAP_SIZE = new
        self.set_sizes()

    def change_tile(self, position, content):
        self.format[position[0]][position[1]] = content

    def is_wall(self, position):
        return self.format[position[0]][position[1]] != "0"  # here safe-points etc also count as walls

    def allow_wall(self, position):
        try:
            for enemy in self.enemies:
                if enemy["type"] == "ep":
                    assert position not in enemy["patrol"][1:]  # not including spawn position (allows enemy deletion)
            return True
        except AssertionError:
            return False

    def clear_tile(self, position):
        # Checking for enemies on the requested tile
        to_delete = []
        for enemy in self.enemies:
            if enemy["type"] == "ep":
                if enemy["patrol"][0] == position:
                    to_delete.append(enemy)
            else:
                if enemy["spawn"] == position:
                    to_delete.append(enemy)

        # Deleting any enemy on the tile
        for enemy in to_delete:
            self.enemies.remove(enemy)

        # Checking Keys to delete
        if position in self.keys:
            self.keys.remove(position)

    def add_key(self, position):
        if position not in self.keys:
            self.keys.append(position)

    def add_random_enemy(self, position):
        if self.get_enemy(position) is None:
            self.enemies.append({
                "type": "er",
                "spawn": position,
            })

    def add_seeker_enemy(self, position):
        if self.get_enemy(position) is None:
            self.enemies.append({
                "type": "es",
                "spawn": position,
            })

    def add_patrol_enemy(self, position):
        if self.get_enemy(position) is None:
            self.enemies.append({
                "type": "ep",
                "patrol": [position],
            })

    def patrol_append(self, spawn, step):
        for enemy in self.enemies:
            if enemy["type"] == "ep":
                if enemy["patrol"][0] == spawn and step != enemy["patrol"][len(enemy["patrol"]) - 1] and step != spawn:
                    # if the correct enemy, and the step isn't equal to the previous one
                    enemy["patrol"].append(step)

    def clear_patrol(self, position):
        for enemy in self.enemies:
            if enemy["type"] == "ep":
                if enemy["patrol"][0] == position:
                    enemy["patrol"] = [position]  # keeping spawn position

    def get_enemy(self, spawn):
        for enemy in self.enemies:
            try:
                if enemy["patrol"][0] == spawn:
                    return enemy
            except KeyError:
                if enemy["spawn"] == spawn:
                    return enemy
