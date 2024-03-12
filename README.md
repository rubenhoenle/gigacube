# Gigacube

This repo is a fork of [mucer/dots_n_boxes](https://github.com/mucer/dots_n_boxes), a project which was done during the [Hacken mit Licht](https://hacken-mit-licht.de) Hackathon.

## Hardware

900 Pixels are available at a density of 60 Pixels per Meter.

The basis of the game is a 25x25x25cm cube. 4 sides of the cube are being used, amounting to 15x15 pixels on each used side:

- 15\*45 pixels in total from left to right
- 15\*15 pixels on the top

The game can be played with 1 (front), 3 (front, top, left) or 4 sides (front, top, left, right).

UP is considered starting by the front side. That means moving UP at the top side corresponds to "to the back".

## Architecture

- For each pixel 2 player states are stored
- A player state contains
  - atPosition: is the player currently at this position?
  - hasTrail: does the player currently have a trail?
  - ownedBy: does player have this pixel captured?
- A pixel can be addressed by 
  - side [0=left, 1=front, 2=right, 3=top]
  - x [0-15]
  - y [0-15]
  - player [0,1]
- The main class is responsible for orchestration
  - Execute a tick every x milliseconds
  - Read controls
  - Play animations
  - Start / end game
  - Render a UI frame (UI can be updated more often per tick to render effects)

## Run commands

|Command|Explanation|
|---|---|
|`deploy/npmCi`|Deploy webserver|
|`reset/cleanEclipse`|Reset game|
|`run/buildCommand`|Start game|
