========================================
Python PyGame Tower Defence Game ReadMe:
========================================
Version 0.8.7b

----------------
In Order To Run:
----------------
Install Python: Written and tested with 2.7.3, on Windows 7

Install PyGame. http://www.pygame.org

Then, just run towerdefense.py

---------------
Files Included:
---------------
Text files:
    changelog.txt - Log of changes.

    options.txt - Is read to determine the values of various options.

    readme.txt - This.

Game files:
    EnemyTypes.py - Holds archetypes of enemies.

    EventFunctions.py - Handles all event calls.

    MainFunctions.py - Handles most of the work directly from the Main loop.

    Rewards.py - Holds bonus functions for completion of maps.

    SenderClass.py - Handles enemy sending, when a new wave is called.

    localclasses.py - Contains many classes used in the game.

    localdefs.py - Contains general functions and variables for use in the game.

        !*!*! NOT SUPPORTED, HAS NOT BEEN UPDATED !*!*!
    mapmaker.py - Used to make custom maps. Run separately!
        !*!*! NOT SUPPORTED, HAS NOT BEEN UPDATED !*!*!

    mapmenu.py - This is for the map selecting menu when starting the game.

    TowerAbilities.py - Holds all the tower upgrades available.

    towerdefense.py - Main game file. RUN THIS TO PLAY.

Folders:
    backgroundimgs/ - Contains images to make up the background and path.

    enemyimgs/ - Contains enemy images. Currently only enemy.png is used.

    mapfiles/ - Contains each 'level's files.

    towerimgs/ - Images for each tower.

    upgradeicons/ - Contains images for upgrade icons.

----------------
Map Maker Guide:
----------------
*Use the 'B' to place the base. Only the last 'B' placed will matter. To save a
    map, you MUST HAVE A BASE!
*Use the flags to set the corners of the paths. Use flag 1 for path 1, etc.
*The first flag for each path is the first corner for that path, the second is
    the second corner, etc.
*There's no way to erase flags or base yet. If you mess up, retry. I recommend
    doing the flags and base first, then do background work.
*Simply click the background tiles to place them on the background.
*When ready to save your map, just hit the 's' key.
*To enter text in these text boxes, hold your curser over them and type.
*The 'map name' is the name of the map and folder you want to save as.
*The Path number boxes, indicate which side of the screen the path will start
    from. For example, if Path 1: is set to 2, then path 1 will come from the
    top of the screen and down to the first flag, turn and go to the second
    flag, etc.

***mapproperties, which includes information about what waves of enemies to
    send, still needs to be done manually!!!
