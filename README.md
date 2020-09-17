# Escape
You are trapped. To escape you must collect all the keys and get to the exit while avoiding all enemy patrols. If they touch you, you're dead.  
*The game also comes with a level editor, allowing you to create and play your own custom levels.*  

For packaged exexutable versions see [here](https://github.com/Ben-Ryder/Escape/releases).

Requirments: For running the source, Python (at least v3) and [pygame](https://www.pygame.org).

## Instructions 
Use the `arrow keys` or `wasd` to move around. When you move over a key, you automatically collect it. When all keys are collected the exit will turn from red to green, and you can go through. However if an enemy touches you at any point you die and fail the level, so make use of the safe points you find, they can't get you there.  
There are 3 kinds of enemy:  
**Patrols**  
The safest enemy, coloured yellow. These follow a set path, if you can figure it out you can avoid them.  
**Random**  
These orange enemies do not have a set patrol. They will randomly move around the map trying to catch you out.  
**Seeker**  
The toughest enemy to outwit. These will chase after you as long as you are out of a safe point.

## Editor
The editor can be used to create custom levels which can then be loaded in and played. Simply pick a tile size and resolution then start adding tiles and enemies. When adding an enemy patrol, if you click and hold for at least 1 second the enemy will pause for that amout of time on the tile.   
If you would like to share any level you make I would be happy to add it into the game. Simply open a feature request [here](https://github.com/Ben-Ryder/Escape/issues).

### Troublshooting
If your level fails to load, check the `main.log` file, it might help point out the problem. If you are still unsure, or think it's a bug let me know. 
Here are a few things to remember:
- The editor won't allow files to be saved in the format `"Level " + x` to prevent conflict with built-in levels.
- If trying to load a file, MAKE SURE TO PRESS LOAD. Pressing save will overwrite that file with a blank map.
- Make sure all patrol points are connected, otherwise the enemy wont be able to get there and it will cause an error.  
*See the bottom of the file `/project/game/level.py` to see the full documentation for levels and validation*  



Ben-Ryder 2019
