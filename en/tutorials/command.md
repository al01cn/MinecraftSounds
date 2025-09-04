---
title: Using Commands
description: How to use commands to play audio in MinecraftSounds
---

# Using Commands to Play Audio

For version 1.7.10 and below:  
`/playsound {soundkey} {player name/target selector} {x} {y} {z} {play range/radius}`  
For version 1.8 and above:  
`/playsound {soundkey} {sound source} {player name/target selector} {x} {y} {z} {play range/radius}`

## soundkey

For details, visit the [Understanding soundkey](/en/tutorials/soundkey) page.

## Sound Source

- `master`: Master volume
- `music`: Music volume
- `record`: Record player [Default choice]
- `weather`: Weather
- `block`: Block
- `neutral`: Neutral entity
- `player`: Player
- `ambient`: Environment
- `voice`: Player voice [Only in higher versions]
- `ui`: User interface [Only in higher versions]

## Target Selector

- `@a`: All players
- `@p`: Nearest player
- `@r`: Random player
- `@s`: Command executor

## Coordinates

- `x`: X-coordinate for audio playback
- `y`: Y-coordinate for audio playback
- `z`: Z-coordinate for audio playback

## Play Range/Radius

- Play range: The range of audio playback, measured in blocks.
- Radius: The radius of audio playback, measured in blocks.

## Examples

- For version 1.7.10 and below:  
`/playsound mcsd.my_sound @a ~ ~ ~ 10000`  
- For version 1.8 and above:  
`/playsound mcsd.my_sound record @a ~ ~ ~ 10000`  

---
# Using Commands to Stop Audio

For version 1.8 and above:  
`/stopsound @a`