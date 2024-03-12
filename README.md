# Gigacube

This repo is a fork of [mucer/dots_n_boxes](https://github.com/mucer/dots_n_boxes), a project which was done during the [Hacken mit Licht](https://hacken-mit-licht.de) Hackathon.

## Gradle (Gigacuberer)

All high business value projects need a gradle project. That's why you can use the following gradle commands for this project:

```bash
./gradlew [deploy|reset|run]
```

## Hardware

900 Pixels are available.
60 Pixels per Meter

Basis of the game is a cube with the size of 25x25x25cm 
4 sides will get 15x15 pixels.

15*45 pixels from left to right
15*15 pixels on the top.

Game is played in 1 (front), 3 (front, top, left) or 4 sides (front, top, left, right).

UP is considered starting by the front side. 
So moving UP at the top side is meaning "to the back".

## Architecture

- For each pixel 2 player states are stored
- A player state contains
  - atPosition: is the player currently at this position
  - hasTrail: the player currently has a trail
  - ownedBy: the player has this pixel captured
- A pixel can be addressed by 
  - side [0=left, 1=front, 2=right, 3=top]
  - x [0-15]
  - y [0-15]
  - player [0,1]
- The main class is responsible for orchestration
  - Execute a tick every x milli seconds
  - Read controls
  - Play animations
  - Start / end game
  - Render a UI frame (UI can be updates more often to per tick to render effects)

## Tasks

- Hardware
  - Build the playground

- Controls
  - Own buttons
  - Serial input from PC
  - Mini Webserver via WIFI
  - Bluetooth controller

- UI
  - Game visualisation
  - Assign LEDs to game plan
  - Special effects (e.g., blinking when area was captured)
  - Idle animation
  - Startdown counter

- Game Logic

- Strech
  - Additional strip that represents the taken area. 20 LEDs and for each 5% a player holds one LED is activated in the color of the player (or 10 LEDs with 10%)
  - Play agains bot
  - Move the box with a serveo depending on the current state of the game (e.g., move areas with a lot of captured boxes in the back)
  - The speed (ticks per second) and/or brighness of the game could be adjusted by a poti
