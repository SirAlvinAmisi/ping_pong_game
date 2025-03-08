# Ping Pong Game

## Overview

This is a simple Ping Pong game built using Python and Tkinter. The game features two paddles controlled by players, a ball that bounces off the walls and paddles, and a scoring system. The first player to reach 5 points wins the game.

## Features

- **Two-player mode**: Player 1 uses `W` and `S` keys to move the left paddle, and Player 2 uses the `Up` and `Down` arrow keys to move the right paddle.
- **Ball physics**: The ball bounces off the top and bottom walls and reverses direction upon paddle contact.
- **Score tracking**: The game keeps track of the score for both players.
- **Gradual difficulty increase**: The ball speed increases after every 7 paddle hits.
- **Restart functionality**: Players can restart the game at any time without speed glitches.

## Installation

1. Ensure you have Python installed on your system (Python 3.6 or later is recommended).
2. Clone or download this repository.
3. Navigate to the project folder.
4. Run the game using the command:
   ```bash
   python ping_pong.py
   ```

## How to Play

- Player 1 controls:
  - Move up: `W`
  - Move down: `S`
- Player 2 controls:
  - Move up: `Up Arrow`
  - Move down: `Down Arrow`
- Restart the game by clicking the **Restart** button.

## Game Rules

- The ball bounces off the top and bottom walls.
- If the ball passes a player's paddle, the opponent gains a point.
- The first player to reach **5 points** wins.
- The game can be restarted at any time.

## Known Issues and Fixes

- **Previous Bug:** Ball speed increased every time the restart button was clicked.
  - **Fix:** The game loop now properly resets the ball speed upon restart.
- **Previous Bug:** Ball speed increased after every score instead of every 7 paddle hits.
  - **Fix:** The hit count is now correctly tracked, and speed only increases after 7 hits.

## Future Enhancements

- Add sound effects for ball bounces and scoring.
- Implement an AI opponent for a single-player mode.
- Improve UI design with better visuals.

## Author

Alvin Amisi Makaya

Enjoy the game! 🚀
