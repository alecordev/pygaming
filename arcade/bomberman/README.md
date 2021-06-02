# Bomberman

Authors: Ricky Cheng, Salvatore DiLeo, Abraham L Fried-Tanzer
Description: Class game of bomberman with single player / multiplayer.

@alecordev: I had to remove all the networking functionality. That requires more refactoring to make it work
(this was using very old libraries that are not up-to-date with current Python)

Single player seems to work fine running `main.py`.

# Original README

## Running the game

- `python main.py`

## Multiplayer

To run this, it is a bit more complicated. Currently it is set to run on the localhost. 
This setting can be modified from the config.py file. In order to run it on your server,
change LOCALHOST = True to LOCALHOST = False. server_tcp, admin, and game file is currently 
set to localhost / reflecting my online server. Those values would have to be changed as well. 

Assuming we are on localhost. You will need to run two separate instances of the game.

## Run the server

- `python ~/bomberman/server_tcp.py`

## Start the two instances of the games, join multiplayer

- `python ~/bomberman/main.py`
- `python ~/bomberman2/main.py`

## Run the admin to start the multiplayer game

- `python ~/bomberman/admin.py`

Press 8 to start the game

## Keys

- Arrow keys to move
- Spacebar to lay bomb
- g is a cheat / easter egg. It adds 1 bomb and 1 power up

## Title Screen

- Single Player
  = One player bomberman, currently set to have 2 stages with 6 levels per stage.

- Multi Player
  = Multiplayer bomberman that supports up to 4 players via a TCP connection. This
    can be played via local

- Instructions
  = Not implemented

- High scores
  = This displays all the high scores for single player.

- Exit
  = Terminates the application.

### BUGS

- Explosion doesn't kill you when you stand on a bomb
- Bomb doesn't display when you press the spacebar / lay it down
- Lag in animation when bomb explodes / player moves around
- When you run into an enemy, it doesn't redraw
- Timer runs out, no calculations
- Stage calculations, after 2-6 it will crash
- Pressing keys does not turn if the player can not move into that position
- Multiplayer, no game over?

```
The MIT License (MIT)

Copyright (c) 2014 Ricky Cheng, Salvatore DiLeo, Abraham L Fried-Tanzer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```